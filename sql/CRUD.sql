/*

CRUD.sql:

Create - Read - Update - Delete. Esse arquivo contêm as operações
de criação de 'entidades' (Create), busca de alguns casos (Read),
atualização de dados (Update) e deleção de tuplas e relações.


Em queries, temos:
> Listar todos os atendimentos de um paciente específico (ordenados por data)
> Listar os procedimentos realizados em um atendimento (com nome do procedimento, quantidade e tempo real)
> Calcular o tempo médio de duração dos atendimentos por residente


*/

-- ─────────────────────────────────────────────────────────────────────────────────────────────────
-- Create's: 

-- não foi testado! 
-- Inserir novo atendimento, verificando existência de paciente, residente e preceptor antes de INSERT
SELECT 
EXISTS (SELECT 1 FROM paciente   WHERE id_pessoa = 1) AS paciente_existe,
EXISTS (SELECT 1 FROM residente  WHERE id_profissional = 12) AS residente_existe,
EXISTS (SELECT 1 FROM preceptor  WHERE id_profissional = 6) AS preceptor_existe;

INSERT INTO atendimento (id_paciente, id_residente, id_preceptor, data_hora, duracao_minutos)
SELECT 1, 13, 6, '2026-07-01 09:00:00', 30
WHERE EXISTS (SELECT 1 FROM paciente WHERE id_pessoa = 1)
AND EXISTS (SELECT 1 FROM residente WHERE id_profissional = 12)
AND EXISTS (SELECT 1 FROM preceptor WHERE id_profissional = 6);


-- ──────────────────────────────────────────────────────────────────────────────────────────────────
-- Read's:

-- Listar todos os atendimentos de um paciente específico (ordenar por data)
SELECT * 
FROM atendimento a
JOIN paciente pc ON a.id_paciente = pc.id_paciente
JOIN pessoa p ON pc.id_paciente = p.id_pessoa
WHERE pc.nome LIKE 'Akemi Almirante' 
-- listar todos os atendimentos de Akemi

ORDER BY data_hora DESC;


-- Listar os procedimentos realizados em um atendimento
SELECT proc.nome, pr.tempo_real, pr.quantidade
FROM procedimento proc
JOIN procedimento_realizado pr ON proc.id_procedimento = pr.id_procedimento
JOIN atendimento a ON a.id_atendimento = pr.id_atendimento
WHERE a.id_atendimento = 10;
-- assume-se um atendimento aleatório para teste


-- Calcular o tempo médio de duração dos atendimentos por residente
SELECT pe.nome AS nome_residente, AVG(a.duracao_minutos) AS media_duracao_minutos
FROM atendimento a
JOIN residente r ON a.id_residente = r.id_residente
JOIN profissional prof ON r.id_residente = prof.id_profissional
JOIN pessoa pe ON prof.id_profissional = pe.id_pessoa
GROUP BY pe.id_pessoa, pe.nome
ORDER BY media_duracao_minutos DESC;


-- ─────────────────────────────────────────────────────────────────────────────────────────────────
-- Update's: 

-- Atualizar os dados de um paciente (num_convenio ou alergias)
UPDATE paciente 
SET num_convenio = 'BRADESCO-99120' AND grupo_sanguineo = 'A+'
WHERE id_paciente = 5;

-- fazer o de alergia

-- ─────────────────────────────────────────────────────────────────────────────────────────────────
-- Delete's:

-- Remover um procedimento realizado (apenas se ainda não houver faturamento associado)



-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
