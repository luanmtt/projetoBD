from datetime import datetime
from database import engine, SessionLocal, Base
import models
import CRUD
from test_cases import popular_banco


# ──────────────────────────────────────────────────────────────────────────────────────────────────


def main():
    popular_banco()

    with SessionLocal() as session:
        atendimentos = CRUD.list_atend(
            session=session, 
            nome_paciente="Akemi Almirante"
        )
        for at in atendimentos:
            print(f"ID: {at.id_atendimento} | Data: {at.data_hora} | Paciente: {at.paciente.nome}")


# ──────────────────────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

