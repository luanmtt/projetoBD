'''

profissionais.py:

ROTAS DA PÁGINA DE PROFISSIONAIS, Blueprint "profissionais".
Lista todos os profissionais (preceptores e residentes).

'''

from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.models import Profissional, Preceptor, Residente
from sqlalchemy import func, case, literal_column
from sqlalchemy.orm import aliased

bp = Blueprint("profissionais", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/profissionais")
def index():
    with SessionLocal() as session:
        total = session.query(func.count(Profissional.id_profissional)).scalar()

        PreceptorAlias = aliased(Preceptor, flat=True)
        ResidenteAlias = aliased(Residente, flat=True)

        rows = (
            session.query(
                Profissional.id_profissional,
                Profissional.nome,
                Profissional.cpf,
                Profissional.telefone,
                Profissional.especialidade,
                Profissional.crm,
                Profissional.data_admissao,
                case(
                    (PreceptorAlias.id_preceptor.isnot(None), literal_column("'Preceptor'")),
                    (ResidenteAlias.id_residente.isnot(None), literal_column("'Residente'")),
                    else_=literal_column("'Profissional'"),
                ).label("tipo"),
            )
            .outerjoin(PreceptorAlias, Profissional.id_profissional == PreceptorAlias.id_preceptor)
            .outerjoin(ResidenteAlias, Profissional.id_profissional == ResidenteAlias.id_residente)
            .order_by(Profissional.id_profissional)
            .all()
        )

        ultimo_log = None

    return render_template(
        "profissionais.html",
        total=total,
        profissionais=rows,
        ultimo_log=ultimo_log,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
