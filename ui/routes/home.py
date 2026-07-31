'''

home.py:

ROTAS DA PÁGINA INICIAL, Blueprint "home" — raiz do site (/).
Por enquanto só renderiza index.html. Depois pode buscar dados
do banco e passar pro template.


'''
from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.models import Paciente, Profissional, Atendimento
from sqlalchemy import func

bp = Blueprint("home", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/")
def index():
   # Abre a conexão com o PostgreSQL
    with SessionLocal() as session:
        # Conta os registros reais usando SQLAlchemy
        total_pacientes = session.query(func.count(Paciente.id_paciente)).scalar()
        total_profissionais = session.query(func.count(Profissional.id_profissional)).scalar()
        total_atendimentos = session.query(func.count(Atendimento.id_atendimento)).scalar()

    # Passa as variáveis para o index.html
    return render_template(
        "index.html",
        total_pacientes=total_pacientes,
        total_profissionais=total_profissionais,
        total_atendimentos=total_atendimentos
    )

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
