from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models import * #incluir tudo?


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# CREATE


#Inserir novo atendimento, verificando existência de paciente, residente e preceptor antes de INSERT
def inserir_atendimento(session: Session, id_paciente, id_residente, id_preceptor,
                         data_hora, duracao_minutos):

    if session.get(Paciente, id_paciente) is None:
        raise ValueError("Paciente não existe")

    if session.get(Residente, id_residente) is None:
        raise ValueError("Residente não existe")

    if session.get(Preceptor, id_preceptor) is None:
        raise ValueError("Preceptor não existe")

    novo = Atendimento(
        id_paciente=id_paciente, id_residente=id_residente,
        id_preceptor=id_preceptor, data_hora=data_hora,
        duracao_minutos=duracao_minutos,
    )
    session.add(novo)
    session.commit()
    return novo


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# READ


def list_atend(session : Session, nome_paciente : str):
    #Listar todos os atendimentos de um paciente específico por nome (ordenados por data decrescente)

    stmt = (
        select(Atendimento)
        .join(Paciente, Atendimento.id_paciente == Paciente.id_paciente)
        .where(Paciente.nome.ilike(f"%{nome_paciente}%"))
        .order_by(Atendimento.data_hora.desc())
    )
    return session.scalars(stmt).all()


def list_proc_atend(session: Session, id_atendimento: int):
    #Listar os procedimentos realizados em um atendimento com nome, quantidade e tempo real
    stmt = (
        select(
            Procedimento.nome,
            ProcedimentoRealizado.tempo_real_minutos,
            ProcedimentoRealizado.quantidade
        )
        .join(ProcedimentoRealizado, Procedimento.id_procedimento == ProcedimentoRealizado.id_procedimento)
        .where(ProcedimentoRealizado.id_atendimento == id_atendimento)
    )
    return session.execute(stmt).all()


def avg_time_atend_por_residente(session: Session):
    #Calcular o tempo médio de duração dos atendimentos por residente.
    stmt = (
        select(
            Residente.nome.label("nome_residente"),
            func.avg(Atendimento.duracao_minutos).label("media_duracao_minutos")
        )
        .join(Residente, Atendimento.id_residente == Residente.id_residente)
        .group_by(Residente.id_residente, Residente.nome)
        .order_by(func.avg(Atendimento.duracao_minutos).desc())
    )
    return session.execute(stmt).all()


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# UPDATE


def atualizar_paciente(session: Session, id_paciente, num_convenio=None, grupo_sanguineo=None, endereco=None):

    paciente = session.get(Paciente, id_paciente)
    if paciente is None:
        raise ValueError("Paciente não existe")

    if num_convenio is not None:
        paciente.num_convenio = num_convenio

    if grupo_sanguineo is not None:
        paciente.grupo_sanguineo = grupo_sanguineo

    if endereco is not None:
        paciente.endereco = endereco  # herdado de pessoa

    session.commit()
    return paciente


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# DELETE


def remover_procedimento_realizado(session: Session, id_atendimento, id_procedimento):

    pr = session.get(ProcedimentoRealizado, (id_atendimento, id_procedimento))
    if pr is None:
        return False

    if pr.faturamento_processado:
        raise ValueError("Não é possível remover: já faturado")

    session.delete(pr)
    session.commit()
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
