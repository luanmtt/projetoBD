#!/usr/bin/env python3
# ────────────────────────────────────────────────────────────────
# RUN.PY — PONTO DE ENTRADA DA APLICAÇÃO
#
# Rode com:  python run.py
# Depois abra: http://localhost:5000
# ────────────────────────────────────────────────────────────────

from ui.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
