from sqlalchemy import select, func
from sqlalchemy.orm import Session, aliased

from models import (
    Pessoa, Paciente, Internacao, Residente, Escala, Plantao, Preceptor,
    Unidade, Atendimento, ProcedimentoRealizado, Procedimento,
)


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# vw_pacientes_internados

def vw_pacientes_internados(session: Session):
    #Pacientes atualmente internados (sem data_hora_saida registrada)
    stmt = (
        select(
            Pessoa.id_pessoa,
            Pessoa.nome,
            Pessoa.data_nascimento,
            Paciente.num_convenio,
            Paciente.grupo_sanguineo,
        )
        .select_from(Paciente)
        .join(Internacao, Internacao.id_paciente == Paciente.id_paciente)
        .join(Pessoa, Paciente.id_paciente == Pessoa.id_pessoa)
        .where(Internacao.data_hora_saida.is_(None))
    )
    return session.execute(stmt).all()


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# vw_residentes_sem_supervisor

def vw_residentes_sem_supervisor(session: Session):
    stmt = (
        select(Pessoa.id_pessoa, Pessoa.nome)
        .select_from(Residente)
        .join(Escala, Escala.id_residente == Residente.id_residente)
        .join(Plantao, Plantao.id_plantao == Escala.id_plantao)
        .join(Pessoa, Pessoa.id_pessoa == Residente.id_residente)
        .outerjoin(Preceptor, Preceptor.id_preceptor == Plantao.id_preceptor)
        .where(
            Preceptor.titulacao.notilike("%doutor%"),
            Preceptor.titulacao.notilike("%dr%"),
        )
    )
    return session.execute(stmt).all()


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# vw_estatisticas_atendimentos_mensal

def vw_estatisticas_atendimentos_mensal(session: Session):
    mes = func.date_trunc("month", Atendimento.data_hora)

    atendimentos_cte = (
        select(
            mes.label("mes"),
            Unidade.nome.label("nome_unidade"),
            func.count(Atendimento.id_atendimento).label("num_atendimentos"),
            func.avg(Atendimento.duracao_minutos).label("media_duracao_min"),
        )
        .join(Unidade, Atendimento.id_unidade == Unidade.id_unidade)
        .group_by(Unidade.nome, mes)
        .cte("atendimentos")
    )

    procedimentos_cte = (
        select(
            Procedimento.nome.label("procedimento"),
            Unidade.nome.label("nome_unidade"),
            mes.label("mes"),
            func.count().label("total_procedimento"),
        )
        .join(Unidade, Atendimento.id_unidade == Unidade.id_unidade)
        .join(ProcedimentoRealizado, Atendimento.id_atendimento == ProcedimentoRealizado.id_atendimento)
        .join(Procedimento, ProcedimentoRealizado.id_procedimento == Procedimento.id_procedimento)
        .group_by(Unidade.nome, mes, Procedimento.nome)
        .cte("procedimentos")
    )

    p1 = aliased(procedimentos_cte)
    p2 = aliased(procedimentos_cte)

    posicao_no_ranking = (
        select(func.count())
        .select_from(p2)
        .where(
            p2.c.nome_unidade == p1.c.nome_unidade,
            p2.c.mes == p1.c.mes,
            p2.c.total_procedimento > p1.c.total_procedimento,
        )
        .scalar_subquery()
    )

    top5_cte = select(p1).where(posicao_no_ranking < 5).cte("top5")

    stmt = (
        select(
            atendimentos_cte.c.nome_unidade,
            atendimentos_cte.c.mes,
            atendimentos_cte.c.num_atendimentos,
            atendimentos_cte.c.media_duracao_min,
            top5_cte.c.procedimento,
            top5_cte.c.total_procedimento,
        )
        .outerjoin(
            top5_cte,
            (atendimentos_cte.c.nome_unidade == top5_cte.c.nome_unidade)
            & (atendimentos_cte.c.mes == top5_cte.c.mes),
        )
        .order_by(
            atendimentos_cte.c.mes,
            atendimentos_cte.c.nome_unidade,
            top5_cte.c.total_procedimento.desc(),
        )
    )
    return session.execute(stmt).all()
