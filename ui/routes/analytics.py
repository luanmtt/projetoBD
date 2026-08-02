'''

analytics.py:

ROTAS DA PÁGINA DE ANALYTICS, Blueprint "analytics".
Executa as consultas avançadas de adv_queries.py e exibe em dropdowns.

'''

from flask import Blueprint, render_template
from orm.database import SessionLocal
from orm.adv_queries import (
    listar_preceptores_is_flamengo,
    listar_ultimo_atendimento,
    percentual_alto_risco_por_residente,
)

bp = Blueprint("analytics", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/analytics")
def index():
    with SessionLocal() as session:
        # 1. Preceptores flamenguistas
        precs = listar_preceptores_is_flamengo(session)
        preceptores_flamengo = [
            {"nome": p.nome, "titulacao": p.titulacao, "crm": p.crm}
            for p in precs
        ]

        # 2. Último atendimento por paciente
        atends = listar_ultimo_atendimento(session)
        ultimos_atendimentos = []
        for a in atends:
            procs = [
                {"nome": pr.procedimento.nome, "quantidade": pr.quantidade}
                for pr in a.procedimentos_realizados
            ]
            ultimos_atendimentos.append({
                "paciente": a.paciente.nome,
                "data_hora": a.data_hora,
                "residente": a.residente.nome,
                "preceptor": a.preceptor.nome,
                "procedimentos": procs,
            })

        # 3. Percentual de alto risco por residente
        estatisticas_risco = percentual_alto_risco_por_residente(session)

    return render_template(
        "analytics.html",
        preceptores_flamengo=preceptores_flamengo,
        ultimos_atendimentos=ultimos_atendimentos,
        estatisticas_risco=estatisticas_risco,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
