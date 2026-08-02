'''

profissionais.py:

ROTAS DA PÁGINA DE PROFISSIONAIS, Blueprint "profissionais".
Lista todos os profissionais e permite cadastro via POST.

'''

from datetime import datetime
from flask import Blueprint, render_template, request, flash
from orm.database import SessionLocal
from orm.models import Profissional, Preceptor, Residente
from sqlalchemy import func, text, case, literal_column
from sqlalchemy.orm import aliased

bp = Blueprint("profissionais", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/profissionais", methods=["GET", "POST"])
def index():
    with SessionLocal() as session:
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            cpf = request.form.get("cpf", "").strip()
            telefone = request.form.get("telefone", "").strip()
            data_nasc = request.form.get("data_nascimento", "").strip()
            endereco = request.form.get("endereco", "").strip()
            especialidade = request.form.get("especialidade", "").strip()
            crm = request.form.get("crm", "").strip()
            data_adm = request.form.get("data_admissao", "").strip()
            tipo = request.form.get("tipo_profissional", "").strip()

            if not all([nome, cpf, telefone, data_nasc, endereco, especialidade, crm, data_adm, tipo]):
                flash("Preencha todos os campos.", "error")
            elif tipo == "preceptor" and not request.form.get("titulacao", "").strip():
                flash("Preencha a titulação.", "error")
            elif tipo == "residente" and not request.form.get("ano_residencia", "").strip():
                flash("Preencha o ano de residência.", "error")
            else:
                session.execute(text("SELECT setval('pessoa_id_pessoa_seq', (SELECT COALESCE(MAX(id_pessoa), 0) FROM pessoa))"))

                prof = None

                if tipo == "preceptor":
                    prof = Preceptor(
                        nome=nome,
                        cpf=cpf,
                        telefone=telefone,
                        data_nascimento=datetime.strptime(data_nasc, "%Y-%m-%d").date(),
                        endereco=endereco,
                        is_flamengo=False,
                        especialidade=especialidade,
                        crm=crm,
                        data_admissao=datetime.strptime(data_adm, "%Y-%m-%d").date(),
                        titulacao=request.form["titulacao"],
                    )
                elif tipo == "residente":
                    prof = Residente(
                        nome=nome,
                        cpf=cpf,
                        telefone=telefone,
                        data_nascimento=datetime.strptime(data_nasc, "%Y-%m-%d").date(),
                        endereco=endereco,
                        is_flamengo=False,
                        especialidade=especialidade,
                        crm=crm,
                        data_admissao=datetime.strptime(data_adm, "%Y-%m-%d").date(),
                        ano_residencia=int(request.form["ano_residencia"]),
                    )

                session.add(prof)
                session.commit()

                session.commit()
                flash("Profissional cadastrado com sucesso!", "success")

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
