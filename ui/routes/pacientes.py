'''

pacientes.py:

ROTAS DA PÁGINA DE PACIENTES, Blueprint "pacientes".
Lista todos os pacientes e permite cadastro via POST.

'''

from datetime import datetime
from flask import Blueprint, render_template, request, flash
from orm.database import SessionLocal
from orm.models import Paciente
from sqlalchemy import func, text

bp = Blueprint("pacientes", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/pacientes", methods=["GET", "POST"])
def index():
    with SessionLocal() as session:
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            cpf = request.form.get("cpf", "").strip()
            telefone = request.form.get("telefone", "").strip()
            data_nasc = request.form.get("data_nascimento", "").strip()
            endereco = request.form.get("endereco", "").strip()
            grupo = request.form.get("grupo_sanguineo", "").strip()
            convenio = request.form.get("num_convenio", "").strip()

            print(f"[DEBUG POST] nome={nome!r} cpf={cpf!r} endereco={endereco!r}")

            if not all([nome, cpf, telefone, data_nasc, endereco, grupo, convenio]):
                flash("Preencha todos os campos.", "error")
            else:
                session.execute(text("SELECT setval('pessoa_id_pessoa_seq', (SELECT COALESCE(MAX(id_pessoa), 0) FROM pessoa))"))

                paciente = Paciente(
                    nome=nome,
                    cpf=cpf,
                    telefone=telefone,
                    data_nascimento=datetime.strptime(data_nasc, "%Y-%m-%d").date(),
                    endereco=endereco,
                    is_flamengo=False,
                    grupo_sanguineo=grupo,
                    num_convenio=convenio,
                )
                session.add(paciente)
                session.commit()
                flash("Paciente cadastrado com sucesso!", "success")

        total = session.query(func.count(Paciente.id_paciente)).scalar()

        pacientes = (
            session.query(Paciente)
            .order_by(Paciente.id_paciente)
            .all()
        )

        ultimo_log = None

    return render_template(
        "pacientes.html",
        total=total,
        pacientes=pacientes,
        ultimo_log=ultimo_log,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
