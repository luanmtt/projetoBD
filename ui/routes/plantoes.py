'''

plantoes.py:

ROTAS DA PÁGINA DE PLANTÕES, Blueprint "plantoes".
Lista todos os plantões e permite reajuste de escala via POST.

'''

from datetime import datetime
from flask import Blueprint, render_template, request, flash
from orm.database import SessionLocal
from orm.models import Plantao, Preceptor, Unidade, Residente, Escala
from orm.procedures import reajustar_escala
from sqlalchemy import func

bp = Blueprint("plantoes", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/plantoes", methods=["GET", "POST"])
def index():
    with SessionLocal() as session:
        if request.method == "POST":
            try:
                qtd = reajustar_escala(
                    session=session,
                    id_residente=int(request.form["id_residente"]),
                    dia_antigo=datetime.strptime(request.form["dia_antigo"], "%Y-%m-%d").date(),
                    turno_antigo=request.form["turno_antigo"],
                    dia_novo=datetime.strptime(request.form["dia_novo"], "%Y-%m-%d").date(),
                    turno_novo=request.form["turno_novo"],
                )
                session.commit()
                flash(f"{qtd} escala(s) reajustada(s) com sucesso!", "success")
            except ValueError as e:
                session.rollback()
                flash(str(e), "error")
            except Exception as e:
                session.rollback()
                flash(f"Erro: {e}", "error")

        total = session.query(func.count(Plantao.id_plantao)).scalar()
        print(f"[DEBUG] Total plantões no banco: {total}")

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

        lista_residentes = (
            session.query(Residente.id_residente, Residente.nome)
            .order_by(Residente.nome)
            .all()
        )

        escalas = (
            session.query(
                Escala.id_escala,
                Plantao.dia_semana,
                Plantao.turno,
                Residente.nome.label("nome_residente"),
                Preceptor.nome.label("nome_preceptor"),
                Unidade.nome.label("nome_unidade"),
            )
            .join(Plantao, Escala.id_plantao == Plantao.id_plantao)
            .join(Residente, Escala.id_residente == Residente.id_residente)
            .join(Preceptor, Plantao.id_preceptor == Preceptor.id_preceptor)
            .join(Unidade, Plantao.id_unidade == Unidade.id_unidade)
            .order_by(Plantao.dia_semana.desc(), Plantao.turno, Residente.nome)
            .all()
        )

    return render_template(
        "plantoes.html",
        total=total,
        plantoes=rows,
        ultimo_log=ultimo_log,
        lista_residentes=lista_residentes,
        escalas=escalas,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
