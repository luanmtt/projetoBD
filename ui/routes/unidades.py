'''

unidades.py:

ROTAS DA PÁGINA DE UNIDADES, Blueprint "unidades".
Exibe unidades e tempo médio de espera global usando calcular_tempo_medio_espera.

'''

from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.procedures import calcular_tempo_medio_espera
from orm.models import Unidade
from sqlalchemy import func

bp = Blueprint("unidades", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/unidades")
def index():
    with SessionLocal() as session:
        total = session.query(func.count(Unidade.id_unidade)).scalar()

        unidades = (
            session.query(Unidade)
            .order_by(Unidade.id_unidade)
            .all()
        )

        tempo_medio = calcular_tempo_medio_espera(session)

    return render_template(
        "unidades.html",
        total=total,
        unidades=unidades,
        tempo_medio=tempo_medio,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
