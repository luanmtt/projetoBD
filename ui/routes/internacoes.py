'''

internacoes.py:

ROTAS DA PÁGINA DE INTERNAÇÕES, Blueprint "internacoes".
Lista internações e permite cadastro/alta via POST.

'''

from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from orm.database import SessionLocal
from orm.models import Internacao, Paciente, Pessoa
from sqlalchemy import func

bp = Blueprint("internacoes", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/internacoes", methods=["GET", "POST"])
def index():
    with SessionLocal() as session:
        if request.method == "POST":
            acao = request.form.get("acao")

            try:
                if acao == "internar":
                    internacao = Internacao(
                        id_paciente=int(request.form["id_paciente"]),
                        data_hora_entrada=datetime.strptime(request.form["data_hora_entrada"], "%Y-%m-%dT%H:%M"),
                        data_hora_saida=None,
                    )
                    session.add(internacao)
                    session.commit()
                    flash("Paciente internado com sucesso!", "success")

                elif acao == "alta":
                    internacao = session.get(Internacao, int(request.form["id_internacao"]))
                    if internacao and internacao.data_hora_saida is None:
                        internacao.data_hora_saida = datetime.now()
                        session.commit()
                        flash("Alta registrada com sucesso!", "success")
                    else:
                        flash("Internação não encontrada ou já teve alta.", "error")

            except Exception as e:
                session.rollback()
                flash(f"Erro: {e}", "error")

        total = session.query(func.count(Internacao.id_internacao)).scalar()

        internacoes = (
            session.query(
                Internacao.id_internacao,
                Internacao.data_hora_entrada,
                Internacao.data_hora_saida,
                Pessoa.nome.label("nome_paciente"),
            )
            .join(Paciente, Internacao.id_paciente == Paciente.id_paciente)
            .join(Pessoa, Paciente.id_paciente == Pessoa.id_pessoa)
            .order_by(Internacao.data_hora_entrada.desc())
            .all()
        )

        lista_pacientes = (
            session.query(Paciente.id_paciente, Pessoa.nome)
            .join(Pessoa, Paciente.id_paciente == Pessoa.id_pessoa)
            .order_by(Pessoa.nome)
            .all()
        )

    return render_template(
        "internacoes.html",
        total=total,
        internacoes=internacoes,
        lista_pacientes=lista_pacientes,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
