'''

pacientes.py:

ROTAS DA PÁGINA DE PACIENTES, Blueprint "pacientes".
Lista todos os pacientes com dados da tabela pessoa.

'''

from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.models import Paciente
from sqlalchemy import func

bp = Blueprint("pacientes", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/pacientes")
def index():
    with SessionLocal() as session:
        total = session.query(func.count(Paciente.id_paciente)).scalar()

        pacientes = (
            session.query(Paciente)
            .order_by(Paciente.id_paciente)
            .all()
        )

        ultimo_log = None

    return render_template(
        "pacientes.html",
        total=total,
        pacientes=pacientes,
        ultimo_log=ultimo_log,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
