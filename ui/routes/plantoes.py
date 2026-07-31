'''

plantoes.py:

ROTAS DA PÁGINA DE PLANTÕES, Blueprint "plantoes".
Lista todos os plantões com nomes de preceptor e unidade.

'''

from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.models import Plantao, Preceptor, Unidade
from sqlalchemy import func

bp = Blueprint("plantoes", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/plantoes")
def index():
    with SessionLocal() as session:
        total = session.query(func.count(Plantao.id_plantao)).scalar()

        rows = (
            session.query(
                Plantao.id_plantao,
                Plantao.dia_semana,
                Plantao.turno,
                Preceptor.nome.label("nome_preceptor"),
                Unidade.nome.label("nome_unidade"),
            )
            .join(Preceptor, Plantao.id_preceptor == Preceptor.id_preceptor)
            .join(Unidade, Plantao.id_unidade == Unidade.id_unidade)
            .order_by(Plantao.dia_semana.desc(), Plantao.turno)
            .all()
        )

        ultimo_log = None

    return render_template(
        "plantoes.html",
        total=total,
        plantoes=rows,
        ultimo_log=ultimo_log,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
