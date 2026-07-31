'''

home.py:

ROTAS DA PÁGINA INICIAL, Blueprint "home" — raiz do site (/).
Por enquanto só renderiza index.html. Depois pode buscar dados
do banco e passar pro template.


'''

from flask import Blueprint, render_template

bp = Blueprint("home", __name__)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@bp.route("/")
def index():
    """
    Página inicial do sistema.
    Renderiza index.html com o layout base.
    """
    return render_template("index.html")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
