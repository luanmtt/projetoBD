/*

analytics.sql:

Esse arquivo contem as operações de consultas analiticas.
Essas são:

-> Ranking dos residentes por número de atendimentos realizados (mostrar nome e total)
-> Listar os preceptores que supervisionaram mais de 5 atendimentos em um determinado mês
-> Para cada unidade, mostrar a quantidade de plantões escalados por residente no mês corrente
-> Listar pacientes que nunca realizaram nenhum procedimento de nível de risco 'ALTO'

*/

-- Consulta ordenada por quantidade de atendimentos realizados
SELECT p.nome AS nome_residente, COUNT(a.id_atendimento) AS total_atendimentos
FROM pessoa p
JOIN residente r ON p.id_pessoa = r.id_residente
JOIN atendimento a ON r.id_residente = a.id_residente

GROUP BY p.id_pessoa, p.nome
ORDER BY total_atendimentos DESC;

-- Lista os preceptores que supervisionaram mais de 5 atendimentos em um determinado mês
SELECT p.nome AS nome_preceptor, COUNT(a.id_atendimento) AS total_atendimentos
FROM pessoa p
JOIN preceptor pr ON pr.id_preceptor = p.id_pessoa
JOIN atendimento a ON pr.id_preceptor = a.id_preceptor
WHERE DATE_TRUNC('month', a.data_hora) = DATE_TRUNC('month', DATE '2026-06-01')
GROUP BY p.id_pessoa, p.nome
HAVING COUNT(a.id_atendimento) > 5
ORDER BY total_atendimentos DESC;

-- Mostrar a quantidade de plantões escalados por residente no mês corrente


SELECT
u.nome AS unidade, p.nome AS nome_residente, COUNT(e.id_escala) AS total_plantoes
FROM escala e
JOIN plantao pl ON e.id_plantao = pl.id_plantao
join unidade u on pl.id_unidade = u.id_unidade
JOIN residente r ON e.id_residente = r.id_residente
JOIN pessoa p ON p.id_pessoa = r.id_residente
-- se ESCALA tiver uma data de referência, filtre pelo mês aqui
GROUP BY u.id_unidade, u.nome, p.id_pessoa, p.nome
ORDER BY u.nome, total_plantoes DESC;

-- Listar pacientes que nunca realizaram nenhum procedimento de nível de risco 'ALTO'

SELECT
p.nome AS nome_paciente
FROM pessoa p
JOIN paciente pac ON pac.id_paciente = p.id_pessoa

WHERE NOT EXISTS (
    SELECT 1
    FROM atendimento a
    JOIN procedimento_realizado pr ON a.id_atendimento = pr.id_atendimento
    JOIN procedimento proc ON pr.id_procedimento = proc.id_procedimento
    JOIN nivel_risco nr ON proc.id_nivel_risco = nr.id_nivel_risco
    WHERE a.id_paciente = pac.id_paciente
      AND nr.nivel = 'ALTO'
);

