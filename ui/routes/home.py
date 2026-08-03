'''
home.py:

ROTA DA PÁGINA INICIAL, Blueprint "home".
Carrega as estatísticas gerais do sistema para a dashboard.
'''

from flask import Blueprint, render_template
from sqlalchemy import func

# Ajuste os imports conforme a estrutura do seu projeto
from orm.database import SessionLocal
from orm.models import Paciente, Profissional, Atendimento

bp = Blueprint("home", __name__)


@bp.route("/")
def index():
    with SessionLocal() as session:
        # Conta o total de registros usando o id como referência (mais rápido)
        total_pacientes = session.query(func.count(Paciente.id_paciente)).scalar()
        total_profissionais = session.query(func.count(Profissional.id_profissional)).scalar()
        total_atendimentos = session.query(func.count(Atendimento.id_atendimento)).scalar()

    # Renderiza o index.html passando as variáveis dinâmicas
    return render_template(
        "index.html",
        total_pacientes=total_pacientes,
        total_profissionais=total_profissionais,
        total_atendimentos=total_atendimentos
    )