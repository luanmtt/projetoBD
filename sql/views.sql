/*


views.sql:

Esse arquivo armazena todas as views requisitadas pelo projeto. Apenas lembrando,
views são relações virtuais, tabelas armazenadas na SGBD do banco como forma de 
evitar várias queries sobre uma coisa muito comum.
Elas são:

    • vw_pacientes_internados: pacientes que estão atualmente internados (data_hora_saida IS NULL na internação mais recente).

    • vw_residentes_sem_supervisor: residentes que estão escalados em algum plantão, mas cujo preceptor não tem titulação de doutor 
                                                                                                                (ou não possui supervisão ativa).

    • vw_estatisticas_atendimentos_mensal: agregação por mês e por unidade: total de atendimentos, média de duração, procedimentos mais comuns.


*/


-- vw_pacientes_internados

CREATE VIEW vw_pacientes_internados AS 
SELECT p.id_pessoa, p.nome, p.data_nascimento, pc.num_convenio, pc.grupo_sanguineo FROM paciente pc 
INNER JOIN internacao it ON it.id_paciente = pc.id_paciente
INNER JOIN pessoa p ON pc.id_paciente = p.id_pessoa
WHERE it.data_hora_saida IS NULL;


-- vw_residentes_sem_supervisor

CREATE VIEW vw_residentes_sem_supervisor AS
SELECT p.id_pessoa, p.nome FROM residente r
INNER JOIN escala es ON r.id_residente = es.id_residente
INNER JOIN plantao pl ON es.id_plantao = pl.id_plantao
INNER JOIN pessoa p ON r.id_residente = p.id_pessoa
LEFT JOIN preceptor pr ON pl.id_preceptor = pr.id_preceptor
WHERE (pr.titulacao NOT ILIKE '%doutor%') AND (pr.titulacao NOT ILIKE '%dr%')
 

-- vw_estatisticas_atendimentos_mensal

CREATE VIEW vw_estatisticas_atendimentos_mensal AS 

WITH atendimentos AS ( 
    SELECT  
            --TO_CHAR(a.data_hora, 'YYYY-MM') AS mes, 
            DATE_TRUNC('month', a.data_hora) AS mes,
            u.nome AS nome_unidade,
            COUNT(a.id_atendimento) AS num_atendimentos,
            AVG(a.duracao_minutos) AS media_duracao_min 

    FROM atendimento a
    INNER JOIN unidade u ON a.id_unidade = u.id_unidade

    GROUP BY u.nome, 
    --TO_CHAR(a.data_hora, 'YYYY-MM')
    DATE_TRUNC('month', a.data_hora)

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
LEFT JOIN top5  
        
        ON at.nome_unidade = top5.nome_unidade
        AND top5.mes = at.mes

ORDER BY at.mes, at.nome_unidade, top5.total_procedimento DESC;


-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
