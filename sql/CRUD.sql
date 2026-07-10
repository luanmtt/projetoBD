-- Inserir novo atendimento

-- Listar todos os atendimentos de um paciente específico (ordenar por data)
SELECT *
FROM atendimento
WHERE id_paciente = 3 --Listar todos os atendimentos de Akemi
ORDER BY data_hora

-- Listar os procedimentos realizados em um atendimento
SELECT p.nome, pr.tempo_real, pr.quantidade
FROM procedimento p
JOIN procedimento_realizado pr ON p.id_procedimento = pr.id_procedimento
JOIN atendimento a ON a.id_atendimento = pr.id_atendimento
WHERE a.id_atendimento = 10

-- Atualizar os dados de um paciente

-- Remover um procedimento realizado

-- Calcular o tempo médio de duração dos atendimentos por residente