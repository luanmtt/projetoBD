from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.adv_queries import percentual_alto_risco_por_residente

bp = Blueprint("analytics", __name__)

@bp.route("/analytics")
def index():
    with SessionLocal() as session:
        # Puxa a sua consulta avançada já pronta
        estatisticas = percentual_alto_risco_por_residente(session)
        
    return render_template("analytics.html", estatisticas=estatisticas)