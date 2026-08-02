'''

atendimentos.py:

ROTAS DA PÁGINA DE ATENDIMENTOS, Blueprint "atendimentos".
Lista todos os atendimentos e permite cadastro via POST
usando registrar_atendimento_completo de orm/procedures.py.

'''

from decimal import Decimal
from datetime import datetime
from flask import Blueprint, render_template, request, flash
from orm.database import SessionLocal
from orm.models import (
    Atendimento, Paciente, Residente, Preceptor, Procedimento,
    Auditoria_atendimento, ProcedimentoRealizado,
)
from orm.procedures import registrar_atendimento_completo
from sqlalchemy import func

bp = Blueprint("atendimentos", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/atendimentos", methods=["GET", "POST"])
def index():
    with SessionLocal() as session:
        if request.method == "POST":
            try:
                data_hora = datetime.strptime(request.form["data_hora"], "%Y-%m-%dT%H:%M")
                duracao = Decimal(request.form["duracao_minutos"])

                procedimentos = [{
                    "id_procedimento": int(request.form["id_procedimento"]),
                    "quantidade": int(request.form["proc_quantidade"]),
                    "observacao": None,
                    "data_hora_inicio": data_hora,
                    "tempo_real_minutos": duracao,
                }]

                registrar_atendimento_completo(
                    session=session,
                    id_paciente=int(request.form["id_paciente"]),
                    id_residente=int(request.form["id_residente"]),
                    id_preceptor=int(request.form["id_preceptor"]),
                    data_hora=data_hora,
                    duracao_minutos=duracao,
                    procedimentos=procedimentos,
                )
                session.commit()
                flash("Atendimento cadastrado com sucesso!", "success")
            except ValueError as e:
                session.rollback()
                flash(str(e), "error")
            except Exception as e:
                session.rollback()
                flash(f"Erro: {e}", "error")

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

        lista_pacientes = (
            session.query(Paciente.id_paciente, Paciente.nome)
            .order_by(Paciente.nome)
            .all()
        )

        lista_residentes = (
            session.query(Residente.id_residente, Residente.nome)
            .order_by(Residente.nome)
            .all()
        )

        lista_preceptores = (
            session.query(Preceptor.id_preceptor, Preceptor.nome)
            .order_by(Preceptor.nome)
            .all()
        )

        lista_procedimentos = (
            session.query(Procedimento.id_procedimento, Procedimento.nome)
            .order_by(Procedimento.nome)
            .all()
        )

    return render_template(
        "atendimentos.html",
        total=total,
        atendimentos=atendimentos,
        ultimo_log=ultimo_log,
        lista_pacientes=lista_pacientes,
        lista_residentes=lista_residentes,
        lista_preceptores=lista_preceptores,
        lista_procedimentos=lista_procedimentos,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
