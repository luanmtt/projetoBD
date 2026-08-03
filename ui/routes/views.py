'''

views.py:

ROTAS DA PÁGINA DE VIEWS, Blueprint "views".
Consulta as views SQL definidas em sql/views.sql.

'''

from flask import Blueprint, render_template
from orm.database import SessionLocal
from sqlalchemy import text

bp = Blueprint("views", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/views")
def index():
    with SessionLocal() as session:
        try:
            pacientes_internados = session.execute(
                text("SELECT * FROM vw_pacientes_internados")
            ).mappings().all()
        except Exception:
            pacientes_internados = []

        try:
            residentes_sem_supervisor = session.execute(
                text("SELECT * FROM vw_residentes_sem_supervisor")
            ).mappings().all()
        except Exception:
            residentes_sem_supervisor = []

        try:
            estatisticas_mensais = session.execute(
                text("SELECT * FROM vw_estatisticas_atendimentos_mensal")
            ).mappings().all()
        except Exception:
            estatisticas_mensais = []

    return render_template(
        "views.html",
        pacientes_internados=pacientes_internados,
        residentes_sem_supervisor=residentes_sem_supervisor,
        estatisticas_mensais=estatisticas_mensais,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
