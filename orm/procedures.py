from datetime import date, datetime
from decimal import Decimal

try:
    from sqlalchemy import select, func, cast, Numeric
    from sqlalchemy.orm import Session
    from orm.models import Paciente, Residente, Preceptor, Atendimento, Procedimento, ProcedimentoRealizado, Escala, Plantao
    from orm.database import SessionLocal
except ImportError:
    from sqlalchemy import select, func, cast, Numeric
    from sqlalchemy.orm import Session
    from models import Paciente, Residente, Preceptor, Atendimento, Procedimento, ProcedimentoRealizado, Escala, Plantao
    from database import SessionLocal

TURNOS_VALIDOS = ("manhã", "tarde", "noite")


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# procedure 1: registra atendimento completo


def registrar_atendimento_completo(
    session: Session,
    id_paciente: int,
    id_residente: int,
    id_preceptor: int,
    data_hora: datetime,
    duracao_minutos: Decimal,
    procedimentos: list[dict],
) -> Atendimento:
    if session.get(Paciente, id_paciente) is None:
        raise ValueError("Paciente não existe")

    if session.get(Residente, id_residente) is None:
        raise ValueError("Residente não existe")

    if session.get(Preceptor, id_preceptor) is None:
        raise ValueError("Preceptor não existe")

    if duracao_minutos is None or duracao_minutos < 0:
        raise ValueError("Duração do atendimento inválida")

    if procedimentos is None or not isinstance(procedimentos, list):
        raise ValueError("A lista de procedimentos deve ser uma lista")

    if len(procedimentos) == 0:
        raise ValueError("O atendimento deve possuir ao menos um procedimento")

    novo_atendimento = Atendimento(
        id_paciente=id_paciente,
        id_residente=id_residente,
        id_preceptor=id_preceptor,
        data_hora=data_hora,
        duracao_minutos=duracao_minutos,
    )
    session.add(novo_atendimento)
    session.flush()

    for proc in procedimentos:
        id_procedimento = proc.get("id_procedimento")
        quantidade = proc.get("quantidade")
        observacao = proc.get("observacao")
        data_hora_inicio = proc.get("data_hora_inicio")
        tempo_real_minutos = proc.get("tempo_real_minutos")

        if session.get(Procedimento, id_procedimento) is None:
            raise ValueError(f"Procedimento {id_procedimento} não existe")

        if quantidade is None or quantidade <= 0:
            raise ValueError(f"Quantidade inválida para o procedimento {id_procedimento}")

        if data_hora_inicio is None:
            raise ValueError(f"Horário de início não informado para o procedimento {id_procedimento}")

        if data_hora_inicio < data_hora:
            raise ValueError(f"O procedimento {id_procedimento} não pode começar antes do atendimento")

        if tempo_real_minutos is None or tempo_real_minutos < 0:
            raise ValueError(f"Tempo real inválido para o procedimento {id_procedimento}")

        session.add(
            ProcedimentoRealizado(
                id_atendimento=novo_atendimento.id_atendimento,
                id_procedimento=id_procedimento,
                quantidade=quantidade,
                observacao=observacao,
                data_hora_inicio=data_hora_inicio,
                tempo_real_minutos=tempo_real_minutos,
                faturamento_processado=False,
            )
        )

    return novo_atendimento


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# procedure 2: calcula o tempo médio de espera global


def calcular_tempo_medio_espera(session: Session):
    primeiro_procedimento = (
        select(
            ProcedimentoRealizado.id_atendimento,
            func.min(ProcedimentoRealizado.data_hora_inicio).label("data_hora_inicio"),
        )
        .group_by(ProcedimentoRealizado.id_atendimento)
        .subquery()
    )

    tempo_espera_segundos = func.extract(
        "epoch",
        primeiro_procedimento.c.data_hora_inicio - Atendimento.data_hora,
    )

    stmt = (
        select(
            func.round(cast(func.avg(tempo_espera_segundos) / 60.0, Numeric), 2).label("tempo_medio_espera_minutos"),
        )
        .join(primeiro_procedimento, primeiro_procedimento.c.id_atendimento == Atendimento.id_atendimento)
    )

    resultado = session.execute(stmt).scalar()
    return resultado


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# procedure 3: reajusta escala de um residente


def reajustar_escala(
    session: Session,
    id_residente: int,
    dia_antigo: date,
    turno_antigo: str,
    dia_novo: date,
    turno_novo: str,
) -> int:
    if session.get(Residente, id_residente) is None:
        raise ValueError("Residente não existe")

    if turno_antigo not in TURNOS_VALIDOS:
        raise ValueError("Turno antigo inválido")

    if turno_novo not in TURNOS_VALIDOS:
        raise ValueError("Turno novo inválido")

    escalas_antigas = session.execute(
        select(Escala, Plantao.id_unidade, Plantao.id_preceptor)
        .join(Plantao, Plantao.id_plantao == Escala.id_plantao)
        .where(
            Escala.id_residente == id_residente,
            Plantao.dia_semana == dia_antigo,
            Plantao.turno == turno_antigo,
        )
    ).all()

    if not escalas_antigas:
        raise ValueError("O residente não possui escala no dia e turno informados")

    ja_tem_escala_no_novo_horario = session.execute(
        select(Escala.id_escala)
        .join(Plantao, Plantao.id_plantao == Escala.id_plantao)
        .where(
            Escala.id_residente == id_residente,
            Plantao.dia_semana == dia_novo,
            Plantao.turno == turno_novo,
        )
    ).first()

    if ja_tem_escala_no_novo_horario is not None:
        raise ValueError("O residente já possui escala no novo dia e turno")

    quantidade_alterada = 0

    for escala, id_unidade, id_preceptor in escalas_antigas:

        novo_plantao = session.execute(
            select(Plantao).where(
                Plantao.id_unidade == id_unidade,
                Plantao.dia_semana == dia_novo,
                Plantao.turno == turno_novo,
            )
        ).scalar_one_or_none()

        if novo_plantao is None:
            novo_plantao = Plantao(
                id_preceptor=id_preceptor,
                id_unidade=id_unidade,
                dia_semana=dia_novo,
                turno=turno_novo,
            )
            session.add(novo_plantao)
            session.flush()

        escala.id_plantao = novo_plantao.id_plantao
        quantidade_alterada += 1

    return quantidade_alterada


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# CLI wrappers


def cli_registrar_atendimento():
    with SessionLocal() as session:
        try:
            registrar_atendimento_completo(
                session=session,
                id_paciente=1,
                id_residente=1,
                id_preceptor=1,
                data_hora=datetime.now(),
                duracao_minutos=Decimal("30.00"),
                procedimentos=[{
                    "id_procedimento": 1,
                    "quantidade": 1,
                    "observacao": None,
                    "data_hora_inicio": datetime.now(),
                    "tempo_real_minutos": Decimal("25.00"),
                }],
            )
            session.commit()
            print("Atendimento cadastrado com sucesso")
        except Exception as e:
            session.rollback()
            print(f"Erro: {e}")


def cli_calcular_tempo_medio():
    with SessionLocal() as session:
        resultado = calcular_tempo_medio_espera(session)
        print(f"Tempo médio de espera global: {resultado} min")


def cli_reajustar_escala():
    with SessionLocal() as session:
        try:
            qtd = reajustar_escala(
                session=session,
                id_residente=1,
                dia_antigo=date(2026, 1, 6),
                turno_antigo="manhã",
                dia_novo=date(2026, 1, 7),
                turno_novo="tarde",
            )
            session.commit()
            print(f"{qtd} escala(s) alterada(s)")
        except Exception as e:
            session.rollback()
            print(f"Erro: {e}")


# ──────────────────────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli_registrar_atendimento()
    cli_calcular_tempo_medio()
    cli_reajustar_escala()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
