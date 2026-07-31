from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func, case
from models import Preceptor, Atendimento, Paciente, ProcedimentoRealizado, Procedimento, Pessoa, Residente, NivelRisco


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# Preceptores que atenderam pacientes flamenguistas 
def listar_preceptores_is_flamengo(session: Session):
    stmt = (
        select(Preceptor)
        .join(Atendimento, Preceptor.id_preceptor == Atendimento.id_preceptor)
        .join(Paciente, Atendimento.id_paciente == Paciente.id_paciente)
        .where(Paciente.is_flamengo == True) 
        .distinct() 
    )
    return session.scalars(stmt).all()



# Exibir o ultimo atendimento de cada paciente
def listar_ultimo_atendimento(session: Session):

    subq = (
        select(
            Atendimento.id_paciente,
            func.max(Atendimento.data_hora).label("ultima_data")
        )
        .group_by(Atendimento.id_paciente)
        .subquery()
    )

    stmt = (
        select(Atendimento)
        .join(
            subq,
            (Atendimento.id_paciente == subq.c.id_paciente) &
            (Atendimento.data_hora == subq.c.ultima_data)
        )
        .options(
            # EAGER LOADING: Carrega os dados aninhados para não gerar novas queries no for-loop
            selectinload(Atendimento.residente),
            selectinload(Atendimento.preceptor),
            selectinload(Atendimento.procedimentos_realizados).selectinload(ProcedimentoRealizado.procedimento)
        )
    )
    return session.scalars(stmt).all()
    

# Calcular o percentual de procedimentos de alto risco realizados por cada residente
def percentual_alto_risco_por_residente(session: Session):

    condicao_alto_risco = case((NivelRisco.nivel == 'ALTO', 1), else_=0)

    stmt = (
        select(
            Residente.id_residente,
            Residente.nome.label("nome_residente"),
            func.count(ProcedimentoRealizado.id_procedimento).label("total"),
            (
                func.sum(condicao_alto_risco) * 100.0 / 
                func.count(ProcedimentoRealizado.id_procedimento)
            ).label("percentual_alto_risco")
        )
        .join(Atendimento, Residente.id_residente == Atendimento.id_residente)
        .join(ProcedimentoRealizado, Atendimento.id_atendimento == ProcedimentoRealizado.id_atendimento)
        .join(Procedimento, ProcedimentoRealizado.id_procedimento == Procedimento.id_procedimento)
        .join(NivelRisco, Procedimento.id_nivel_risco == NivelRisco.id_nivel_risco)
        .group_by(Residente.id_residente, Residente.nome)
    )
    
    return session.execute(stmt).all()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
