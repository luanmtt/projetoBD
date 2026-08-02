import threading
import time
from datetime import datetime
from pathlib import Path

from sqlalchemy import select, delete, text
from sqlalchemy.exc import IntegrityError

from database import SessionLocal
from models import Escala, Plantao


ID_PLANTAO_DEMO = 1
ID_RESIDENTE_DEMO = 11

LOG_FILE = Path(__file__).parent / "concurrency_log.txt"


def log(nome_thread: str, mensagem: str) -> None:

    agora = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    linha = f"[{agora}] [{nome_thread:<10}] {mensagem}"
    print(linha)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


def _limpar_escala_demo() -> None:
    with SessionLocal() as session:
        session.execute(
            delete(Escala).where(
                Escala.id_plantao == ID_PLANTAO_DEMO,
                Escala.id_residente == ID_RESIDENTE_DEMO,
            )
        )
        session.commit()


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# lock pessimista

def _pessimista(nome_thread: str, barreira: threading.Barrier) -> None:
    with SessionLocal() as session:
        log(nome_thread, "esperando a outra thread para tentarmos o lock juntas...")
        barreira.wait()

        log(nome_thread, "tentando obter lock (SELECT ... FOR UPDATE) no plantão...")

        plantao = session.execute(
            select(Plantao).where(Plantao.id_plantao == ID_PLANTAO_DEMO).with_for_update()
        ).scalar_one_or_none()

        if not plantao:
            log(nome_thread, " plantão não encontrado.")
            return

        log(nome_thread, " lock obtido com sucesso.")

        ja_escalado = session.execute(
            select(Escala.id_escala).where(
                Escala.id_plantao == ID_PLANTAO_DEMO,
                Escala.id_residente == ID_RESIDENTE_DEMO,
            )
        ).first()

        if ja_escalado:
            log(nome_thread, " outra transação já escalou esse residente enquanto eu esperava o lock. Abortando.")
            session.rollback()
            return

        time.sleep(0.5)

        try:
            session.add(Escala(id_plantao=ID_PLANTAO_DEMO, id_residente=ID_RESIDENTE_DEMO))
            session.commit()
            log(nome_thread, " INSERT feito com sucesso, lock liberado no commit.")
        except IntegrityError:
            session.rollback()
            log(nome_thread, " erro de integridade (duplicidade no banco).")


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# lock otimista

def _otimista(nome_thread: str, barreira: threading.Barrier, max_tentativas: int = 3) -> None:
    for tentativa in range(1, max_tentativas + 1):
        with SessionLocal() as session:
            res = session.execute(
                text("SELECT xmin::text FROM plantao WHERE id_plantao = :id"),
                {"id": ID_PLANTAO_DEMO}
            ).fetchone()

            if not res:
                log(nome_thread, " plantão não encontrado. Abortando.")
                return

            xmin_lido = res[0]
            log(nome_thread, f"tentativa {tentativa}: li o plantão com xmin={xmin_lido}")

            ja_escalado = session.execute(
                select(Escala.id_escala).where(
                    Escala.id_plantao == ID_PLANTAO_DEMO,
                    Escala.id_residente == ID_RESIDENTE_DEMO,
                )
            ).first()

            if ja_escalado:
                log(nome_thread, " residente já escalado (visto na releitura). Abortando.")
                return

            if tentativa == 1:
                barreira.wait()

            result = session.execute(
                text("UPDATE plantao SET id_unidade = id_unidade WHERE id_plantao = :id AND xmin::text = :xmin"),
                {"id": ID_PLANTAO_DEMO, "xmin": xmin_lido}
            )

            if result.rowcount == 0:
                session.rollback()
                log(nome_thread, " conflito otimista: outro processo alterou o plantão (xmin desatualizado). Tentando de novo...")
                time.sleep(0.05)
                continue

            log(nome_thread, " validação otimista aceita")

            try:
                session.add(Escala(id_plantao=ID_PLANTAO_DEMO, id_residente=ID_RESIDENTE_DEMO))
                session.commit()
                log(nome_thread, " commit final ok.")
                return
            except IntegrityError:
                session.rollback()
                log(nome_thread, " erro de integridade: residente já inserido por outra transação.")
                return

    log(nome_thread, " excedeu o número de tentativas, desistindo.")


# ──────────────────────────────────────────────────────────────────────────────────────────────────

def rodar_cenario(titulo: str, funcao_tentativa) -> None:
    separador = "\n" + "═" * 100
    bloco = f"{separador}\n{titulo}\n{'═' * 100}"
    print(bloco)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(bloco + "\n")

    _limpar_escala_demo()

    barreira = threading.Barrier(2)
    t1 = threading.Thread(target=funcao_tentativa, args=("Thread-A", barreira), name="Thread-A")
    t2 = threading.Thread(target=funcao_tentativa, args=("Thread-B", barreira), name="Thread-B")

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    with SessionLocal() as session:
        total = session.execute(
            select(Escala.id_escala).where(
                Escala.id_plantao == ID_PLANTAO_DEMO,
                Escala.id_residente == ID_RESIDENTE_DEMO,
            )
        ).all()

    status = "consistente" if len(total) == 1 else "inconsistente"
    resultado = f"\n>> resultado final: {len(total)} linha(s) de escala para o residente {ID_RESIDENTE_DEMO} no plantão {ID_PLANTAO_DEMO} (esperado: 1) — {status}"
    print(resultado)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(resultado + "\n")


if __name__ == "__main__":
    LOG_FILE.write_text("", encoding="utf-8")
    rodar_cenario("LOCK PESSIMISTA", _pessimista)
    rodar_cenario("LOCK OTIMISTA", _otimista)
    print(f"\nLog exportado para: {LOG_FILE}")
