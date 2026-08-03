#!/usr/bin/env python3
# ────────────────────────────────────────────────────────────────
# RUN.PY — PONTO DE ENTRADA DA APLICAÇÃO
#
# Rode com:
#   python run.py --original   # recria tudo do zero (drop + create + dados de teste)
#   python run.py --current    # roda com o banco existente (padrão)
#   python run.py              # equivalente a --current
#
# Depois abra: http://localhost:5000
# ────────────────────────────────────────────────────────────────

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.app import create_app


def run_original():
    """Recria o banco do zero e popula com dados de teste."""
    from orm.database import engine, SessionLocal, Base
    from sqlalchemy import text
    import orm.models as models

    print("[run.py] Dropando views e auditoria...")
    with engine.connect() as conn:
        conn.execute(text("DROP VIEW IF EXISTS vw_pacientes_internados CASCADE"))
        conn.execute(text("DROP VIEW IF EXISTS vw_residentes_sem_supervisor CASCADE"))
        conn.execute(text("DROP VIEW IF EXISTS vw_estatisticas_atendimentos_mensal CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS auditoria_atendimento CASCADE"))
        conn.commit()

    print("[run.py] Dropando todas as tabelas...")
    Base.metadata.drop_all(bind=engine)

    print("[run.py] Criando tabelas...")
    Base.metadata.create_all(bind=engine)

    print("[run.py] Recriando views...")
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE VIEW vw_pacientes_internados AS 
            SELECT p.id_pessoa, p.nome, p.data_nascimento, pc.num_convenio, pc.grupo_sanguineo 
            FROM paciente pc 
            INNER JOIN internacao it ON it.id_paciente = pc.id_paciente
            INNER JOIN pessoa p ON pc.id_paciente = p.id_pessoa
            WHERE it.data_hora_saida IS NULL
        """))
        conn.execute(text("""
            CREATE VIEW vw_residentes_sem_supervisor AS
            SELECT p.id_pessoa, p.nome FROM residente r
            INNER JOIN escala es ON r.id_residente = es.id_residente
            INNER JOIN plantao pl ON es.id_plantao = pl.id_plantao
            INNER JOIN pessoa p ON r.id_residente = p.id_pessoa
            LEFT JOIN preceptor pr ON pl.id_preceptor = pr.id_preceptor
            WHERE (pr.titulacao NOT ILIKE '%doutor%') AND (pr.titulacao NOT ILIKE '%dr%')
        """))
        conn.execute(text("""
            CREATE VIEW vw_estatisticas_atendimentos_mensal AS 
            WITH atendimentos AS ( 
                SELECT  
                    DATE_TRUNC('month', a.data_hora) AS mes,
                    u.nome AS nome_unidade,
                    COUNT(a.id_atendimento) AS num_atendimentos,
                    AVG(a.duracao_minutos) AS media_duracao_min 
                FROM atendimento a
                INNER JOIN unidade u ON a.id_unidade = u.id_unidade
                GROUP BY u.nome, DATE_TRUNC('month', a.data_hora)
            ), procedimentos AS ( 
                SELECT 
                    p.nome AS procedimento,
                    u.nome AS nome_unidade,
                    DATE_TRUNC('month', a.data_hora) AS mes,    
                    COUNT(*) AS total_procedimento
                FROM atendimento a
                INNER JOIN unidade u ON a.id_unidade = u.id_unidade
                INNER JOIN procedimento_realizado pr ON a.id_atendimento = pr.id_atendimento
                INNER JOIN procedimento p ON pr.id_procedimento = p.id_procedimento
                GROUP BY u.nome, DATE_TRUNC('month', a.data_hora), p.nome
            ), top5 AS (
                SELECT p1.*
                FROM procedimentos p1
                WHERE (
                    SELECT COUNT(*)
                    FROM procedimentos p2
                    WHERE p2.nome_unidade = p1.nome_unidade
                      AND p2.mes = p1.mes
                      AND p2.total_procedimento > p1.total_procedimento
                ) < 5
            )
            SELECT 
                at.nome_unidade,
                at.mes,
                at.num_atendimentos,
                at.media_duracao_min,
                top5.procedimento,
                top5.total_procedimento
            FROM atendimentos at 
            LEFT JOIN top5 ON at.nome_unidade = top5.nome_unidade AND top5.mes = at.mes
            ORDER BY at.mes, at.nome_unidade, top5.total_procedimento DESC
        """))
        conn.commit()

    print("[run.py] Populando com dados de teste...")
    from orm.test_cases import popular_banco
    popular_banco()

    print("[run.py] Resetando sequences...")
    with engine.connect() as conn:
        for table, col in [
            ("pessoa", "id_pessoa"),
            ("unidade", "id_unidade"),
            ("nivel_risco", "id_nivel_risco"),
            ("procedimento", "id_procedimento"),
            ("alergia", "id_alergia"),
            ("atendimento", "id_atendimento"),
            ("plantao", "id_plantao"),
            ("escala", "id_escala"),
            ("internacao", "id_internacao"),
            ("auditoria_atendimento", "id_auditoria"),
        ]:
            conn.execute(text(
                f"SELECT setval('{table}_{col}_seq', (SELECT COALESCE(MAX({col}), 0) FROM {table}))"
            ))
        conn.commit()

    print("[run.py] Banco recriado com sucesso!")


def run_current():
    """Apenas inicia o servidor com o banco existente."""
    print("[run.py] Iniciando com banco existente...")


if __name__ == "__main__":
    flag = sys.argv[1] if len(sys.argv) > 1 else "--current"

    if flag == "--original":
        run_original()
    elif flag == "--current":
        run_current()
    else:
        print(f"[run.py] Flag desconhecida: {flag}")
        print("  Use: python run.py --original  (recria tudo)")
        print("  Use: python run.py --current   (banco existente)")
        sys.exit(1)

    app = create_app()
    app.run(debug=True, port=5000)
