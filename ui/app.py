'''
    
app.py:

Cria a instância do Flask, registra os blueprints (rotas)
e fecha a sessão do banco depois de cada requisição.


'''

import os
import sys

# Garante que o diretório ui/ esteja no path de imports do Python.
# Assim `from routes.home import bp` funciona mesmo rodando da raiz.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def create_app():
    """
    Cria e configura a aplicação Flask.

    Configura também as pastas de template e arquivos estáticos,
    que ficam dentro de ui/.
    """

    ui_dir = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(ui_dir, "templates"),
        static_folder=os.path.join(ui_dir, "static"),
    )
    

    ''' ──────────────────────────────────────────────────────────────────────────────────────────────────
     • Blueprints (rotas): Cada arquivo em routes/ registra seu prefixo aqui.
    '''

    from routes.home import bp as home_bp
    app.register_blueprint(home_bp)

    from routes.pacientes import bp as pacientes_bp
    app.register_blueprint(pacientes_bp)

    from routes.profissionais import bp as profissionais_bp
    app.register_blueprint(profissionais_bp)

    from routes.atendimentos import bp as atendimentos_bp
    app.register_blueprint(atendimentos_bp)

    from routes.plantoes import bp as plantoes_bp
    app.register_blueprint(plantoes_bp)

    return app


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
