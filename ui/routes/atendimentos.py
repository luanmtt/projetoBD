'''

atendimentos.py:

ROTAS DA PÁGINA DE ATENDIMENTOS, Blueprint "atendimentos".
Lista todos os atendimentos com nomes de paciente, residente e preceptor.

'''

from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.models import (
    Atendimento, Paciente, Residente, Preceptor,
    Auditoria_atendimento, ProcedimentoRealizado, Procedimento,
)
from sqlalchemy import func

bp = Blueprint("atendimentos", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/atendimentos")
def index():
    with SessionLocal() as session:
        total = session.query(func.count(Atendimento.id_atendimento)).scalar()

        rows = (
            session.query(
                Atendimento.id_atendimento,
                Atendimento.data_hora,
                Atendimento.duracao_minutos,
                Paciente.nome.label("nome_paciente"),
                Residente.nome.label("nome_residente"),
                Preceptor.nome.label("nome_preceptor"),
            )
            .join(Paciente, Atendimento.id_paciente == Paciente.id_paciente)
            .join(Residente, Atendimento.id_residente == Residente.id_residente)
            .join(Preceptor, Atendimento.id_preceptor == Preceptor.id_preceptor)
            .order_by(Atendimento.data_hora.desc())
            .all()
        )

        atendimento_ids = [r.id_atendimento for r in rows]

        proc_rows = (
            session.query(
                ProcedimentoRealizado.id_atendimento,
                Procedimento.nome.label("proc_nome"),
                Procedimento.codigo.label("proc_codigo"),
                ProcedimentoRealizado.quantidade,
                ProcedimentoRealizado.tempo_real_minutos,
            )
            .join(Procedimento, ProcedimentoRealizado.id_procedimento == Procedimento.id_procedimento)
            .filter(ProcedimentoRealizado.id_atendimento.in_(atendimento_ids))
            .all()
        )

        proc_map = {}
        for pr in proc_rows:
            proc_map.setdefault(pr.id_atendimento, []).append(pr)

        atendimentos = []
        for r in rows:
            atendimentos.append({
                "id_atendimento": r.id_atendimento,
                "data_hora": r.data_hora,
                "duracao_minutos": r.duracao_minutos,
                "nome_paciente": r.nome_paciente,
                "nome_residente": r.nome_residente,
                "nome_preceptor": r.nome_preceptor,
                "procedimentos": proc_map.get(r.id_atendimento, []),
            })

        ultimo_log = (
            session.query(Auditoria_atendimento)
            .order_by(Auditoria_atendimento.data_hora.desc())
            .first()
        )

    return render_template(
        "atendimentos.html",
        total=total,
        atendimentos=atendimentos,
        ultimo_log=ultimo_log,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
