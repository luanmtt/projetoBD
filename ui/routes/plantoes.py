'''

plantoes.py:

ROTAS DA PÁGINA DE PLANTÕES, Blueprint "plantoes".
Lista todos os plantões e permite reajuste de escala via POST.

'''

from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from orm.database import SessionLocal
from orm.models import Plantao, Preceptor, Unidade, Residente, Escala, Escala
from orm.procedures import reajustar_escala
from sqlalchemy import func

bp = Blueprint("plantoes", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/plantoes/delete_plantao/<int:id>", methods=["POST"])
def delete_plantao(id):
    with SessionLocal() as session:
        try:
            plantao = session.get(Plantao, id)
            if plantao:
                session.delete(plantao)
                session.commit()
                flash("Plantão removido com sucesso!", "success")
            else:
                flash("Plantão não encontrado.", "error")
        except Exception as e:
            session.rollback()
            flash(f"Erro ao remover: {e}", "error")
    return redirect(url_for("plantoes.index"))


@bp.route("/plantoes/delete_escala/<int:id>", methods=["POST"])
def delete_escala(id):
    with SessionLocal() as session:
        try:
            escala = session.get(Escala, id)
            if escala:
                session.delete(escala)
                session.commit()
                flash("Escala removida com sucesso!", "success")
            else:
                flash("Escala não encontrada.", "error")
        except Exception as e:
            session.rollback()
            flash(f"Erro ao remover: {e}", "error")
    return redirect(url_for("plantoes.index"))


@bp.route("/plantoes/add_plantao", methods=["POST"])
def add_plantao():
    with SessionLocal() as session:
        try:
            plantao = Plantao(
                id_preceptor=int(request.form["id_preceptor"]),
                id_unidade=int(request.form["id_unidade"]),
                dia_semana=datetime.strptime(request.form["dia_semana"], "%Y-%m-%d").date(),
                turno=request.form["turno"],
            )
            session.add(plantao)
            session.commit()
            flash("Plantão adicionado com sucesso!", "success")
        except Exception as e:
            session.rollback()
            flash(f"Erro: {e}", "error")
    return redirect(url_for("plantoes.index"))


@bp.route("/plantoes/add_escala", methods=["POST"])
def add_escala():
    with SessionLocal() as session:
        try:
            escala = Escala(
                id_plantao=int(request.form["id_plantao"]),
                id_residente=int(request.form["id_residente"]),
            )
            session.add(escala)
            session.commit()
            flash("Escala adicionada com sucesso!", "success")
        except Exception as e:
            session.rollback()
            flash(f"Erro: {e}", "error")
    return redirect(url_for("plantoes.index"))


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

        lista_residentes = (
            session.query(Residente.id_residente, Residente.nome)
            .order_by(Residente.nome)
            .all()
        )

        lista_preceptores = (
            session.query(Preceptor.id_preceptor, Preceptor.nome)
            .order_by(Preceptor.nome)
            .all()
        )

        lista_unidades = (
            session.query(Unidade.id_unidade, Unidade.nome)
            .order_by(Unidade.nome)
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
        lista_residentes=lista_residentes,
        lista_preceptores=lista_preceptores,
        lista_unidades=lista_unidades,
        escalas=escalas,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
