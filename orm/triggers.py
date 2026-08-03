from datetime import date, datetime
from decimal import Decimal

try:
    from sqlalchemy import event, select, insert, update, func, inspect
    from sqlalchemy.orm import Session
    from orm.models import Escala, Plantao, Atendimento, Auditoria_atendimento, ProcedimentoRealizado, Procedimento
except ImportError:
    from sqlalchemy import event, select, insert, update, func, inspect
    from sqlalchemy.orm import Session
    from models import Escala, Plantao, Atendimento, Auditoria_atendimento, ProcedimentoRealizado, Procedimento


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# helpers de serialização

def _valor_serializavel(valor):
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, Decimal):
        return float(valor)
    return valor


def _serializa_linha(obj):
    if obj is None:
        return None
    insp = inspect(obj)
    return {
        attr.key: _valor_serializavel(getattr(obj, attr.key))
        for attr in insp.mapper.column_attrs
    }


def _serializa_linha_antiga(obj):
    insp = inspect(obj)
    dados = {}
    for attr in insp.mapper.column_attrs:
        historico = getattr(insp.attrs, attr.key).history
        if historico.deleted:
            dados[attr.key] = _valor_serializavel(historico.deleted[0])
        else:
            dados[attr.key] = _valor_serializavel(getattr(obj, attr.key))
    return dados


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# trg_check_sobreposicao_escala

@event.listens_for(Session, "before_flush")
def _checar_sobreposicao_escala(session, flush_context, instances):
    alvos = [obj for obj in (list(session.new) + list(session.dirty)) if isinstance(obj, Escala)]

    for escala in alvos:
        plantao_novo = session.get(Plantao, escala.id_plantao)
        if plantao_novo is None:
            continue

        print(f"[TRIGGER] trg_check_sobreposicao_escala: verificando residente {escala.id_residente} no plantão {escala.id_plantao}")

        condicoes = [
            Escala.id_residente == escala.id_residente,
            Plantao.turno == plantao_novo.turno,
            Plantao.dia_semana == plantao_novo.dia_semana,
            Plantao.id_unidade != plantao_novo.id_unidade,
        ]
        if escala.id_escala is not None:
            condicoes.append(Escala.id_escala != escala.id_escala)

        stmt = (
            select(Escala.id_escala)
            .join(Plantao, Escala.id_plantao == Plantao.id_plantao)
            .where(*condicoes)
        )

        conflito = session.execute(stmt).first()

        if conflito is not None:
            print(f"[TRIGGER] trg_check_sobreposicao_escala: CONFLITO — residente {escala.id_residente} já escalado em outra unidade")
            raise ValueError(
                f"Residente {escala.id_residente} já está escalado no dia "
                f"{plantao_novo.dia_semana} turno {plantao_novo.turno} em outra unidade."
            )

        print(f"[TRIGGER] trg_check_sobreposicao_escala: OK — sem conflito")


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# trg_audita_atendimento

def _audita_insercao(mapper, connection, target: Atendimento):
    usuario = connection.execute(select(func.current_user())).scalar()
    print(f"[TRIGGER] trg_audita_atendimento: INSERT no atendimento {target.id_atendimento} por {usuario}")
    connection.execute(
        insert(Auditoria_atendimento.__table__).values(
            id_atendimento=target.id_atendimento,
            data_hora=datetime.now(),
            operacao="INSERT",
            usuario=usuario,
            dados_novos=_serializa_linha(target),
            dados_antigos=None,
        )
    )


def _audita_atualizacao(mapper, connection, target: Atendimento):
    usuario = connection.execute(select(func.current_user())).scalar()
    print(f"[TRIGGER] trg_audita_atendimento: UPDATE no atendimento {target.id_atendimento} por {usuario}")
    connection.execute(
        insert(Auditoria_atendimento.__table__).values(
            id_atendimento=target.id_atendimento,
            data_hora=datetime.now(),
            operacao="UPDATE",
            usuario=usuario,
            dados_novos=_serializa_linha(target),
            dados_antigos=_serializa_linha_antiga(target),
        )
    )


def _audita_delecao(mapper, connection, target: Atendimento):
    usuario = connection.execute(select(func.current_user())).scalar()
    print(f"[TRIGGER] trg_audita_atendimento: DELETE no atendimento {target.id_atendimento} por {usuario}")
    connection.execute(
        insert(Auditoria_atendimento.__table__).values(
            id_atendimento=target.id_atendimento,
            data_hora=datetime.now(),
            operacao="DELETE",
            usuario=usuario,
            dados_novos=None,
            dados_antigos=_serializa_linha(target),
        )
    )


event.listen(Atendimento, "after_insert", _audita_insercao)
event.listen(Atendimento, "after_update", _audita_atualizacao)
event.listen(Atendimento, "before_delete", _audita_delecao)


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# trg_atualiza_media_procedimentos

def _atualiza_media_procedimento(mapper, connection, target: ProcedimentoRealizado):
    print(f"[TRIGGER] trg_atualiza_media_procedimentos: atualizando média do procedimento {target.id_procedimento}")

    tabela_pr = ProcedimentoRealizado.__table__

    nova_media = connection.execute(
        select(func.avg(tabela_pr.c.tempo_real_minutos))
        .where(tabela_pr.c.id_procedimento == target.id_procedimento)
    ).scalar()

    connection.execute(
        update(Procedimento.__table__)
        .where(Procedimento.__table__.c.id_procedimento == target.id_procedimento)
        .values(media_tempo_procedimento=nova_media)
    )

    print(f"[TRIGGER] trg_atualiza_media_procedimentos: nova média = {nova_media}")


event.listen(ProcedimentoRealizado, "after_insert", _atualiza_media_procedimento)
