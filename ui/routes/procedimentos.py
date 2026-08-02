from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.models import Procedimento

bp = Blueprint("procedimentos", __name__)

@bp.route("/procedimentos")
def index():
    with SessionLocal() as session:
        # Busca todos os procedimentos cadastrados no banco
        procedimentos = session.query(Procedimento).order_by(Procedimento.id_procedimento).all()
        
    return render_template("procedimentos.html", procedimentos=procedimentos)