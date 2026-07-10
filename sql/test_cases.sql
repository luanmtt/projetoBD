/*

test_cases.sql:

Esse arquivo contêm as entries de teste que o sistema demanda para funcionar. assim como especificado
no projeto, serão adicionados 5 pacientes, 5 residentes, 5 preceptores, 3 unidades, 10 atendimentos e 10 procedimentos realizados

*/

-- add Pessoas
INSERT INTO pessoa(id_pessoa, nome, cpf, data_nascimento, is_flamengo, telefone )
VALUES
	(1, 'Luan Motta', '210.113.954-60', '01/10/44', FALSE, '55(81)95509-5100'),
    (2, 'Lucas Schettini', '196.685.636-70', '27/05/28', TRUE, '55(71)93284-2315'),
    (3, 'Akemi Almirante', '742.807.130-58', '10/04/52', FALSE, '55(11)91853-9648'),
    (4, 'Andrei Maia', '852.159.098-30', '20/12/53', TRUE, '55(71)93522-5986'),
    (5, 'Marlon Neto', '837.851.729-77', '26/08/16', TRUE, '55(51)97295-3461'),
    (6, 'Marcelo Iury', '400.878.351-11', '16/09/22', TRUE, '55(71)95858-7524'),
    (7, 'Neymar Jr', '461.301.397-10', '03/04/96', FALSE, '55(41)95727-5013'),
    (8, 'Michael Scott', '634.706.010-18', '12/01/73', TRUE, '55(85)96173-5506'),
    (9, 'Clark Kent', '826.526.064-04', '02/11/43', TRUE, '55(91)97894-7684'),
    (10, 'Bob Jackson', '156.786.184-88', '12/12/80', FALSE, '55(41)94083-6938'),
    (11, 'Alice Kennedy', '130.776.889-76', '09/11/29', TRUE, '55(51)98561-9000'),
	(12, 'Drauzio Varella', '085.784.728-33', '09/11/11', FALSE, '55(85)92621-7758'),
    (13, 'Oswaldo Cruz', '491.691.164-83', '03/05/29', FALSE, '55(85)97973-7039'),
    (14, 'Antônio de Salles', '981.246.846-10', '14/01/92', FALSE, '55(71)93021-1378'),
    (15, 'Angelita Habr-Gama ', '937.898.585-55', '24/11/23', FALSE, '55(71)93537-1108');

-- especialização de Pacientes
INSERT INTO paciente(id_pessoa, num_convenio, grupo_sanguineo)
VALUES
    (1, 'UNIMED-88213', 'O+'),
    (2, 'BRADESCO-44210', 'A-'),
    (3, 'AMIL-90911', 'B+'),
    (4, 'SULAMERICA-11290', 'AB+'),
    (5, 'UNIMED-77102', 'O-');

-- especialização de Profissionais
INSERT INTO profissional(id_pessoa, CRM, data_admissao, especialidade)
VALUES
    (6, 'CRM-PB 12345', '2015-03-01', 'Ortopedia'), -- 5 preceptores
    (7, 'CRM-PB 22344', '2016-07-10', 'Oncologia'),
    (8, 'CRM-PB 33456', '2012-01-15', 'Cirurgia Geral'),
    (9, 'CRM-PB 44567', '2018-09-01', 'Clínica Médica'),
    (10, 'CRM-PB 55678', '2010-05-20', 'Emergência'),
    (11, 'CRM-PB 66789', '2023-02-01', 'Ortopedia'), -- 5 residentes
    (12, 'CRM-PB 77890', '2022-08-15', 'Oncologia'),
    (13, 'CRM-PB 88901', '2024-01-10', 'Cirurgia Geral'),
    (14, 'CRM-PB 99012', '2023-06-01', 'Clínica Médica'),
    (15, 'CRM-PB 10123', '2021-03-01', 'Emergência');

-- especialização de Preceptores
INSERT INTO preceptor(id_profissional, titulacao)
VALUES
    (6, 'Chopper'),
    (7, 'Mestre'),
    (8, 'Doutor'),
    (9, 'Especialista'),
    (10, 'Doutor');

-- especialização de Residentes
INSERT INTO residente(id_profissional, ano_residencia)
VALUES
    (11, 1),
    (12, 2),
    (13, 1),
    (14, 3),
    (15, 2);

-- unidades 
INSERT INTO unidade(id_unidade, nome, tipo, capacidade_leitos)
VALUES
	(1, 'Trauminha','Emergência Ortotraumatológica',55),
	(2, 'Oncologia','Tratamento de Câncer',18),
	(3, 'Centro Cirúrgico','Cirurgia',40),
	-- ('Centro de Observação', 'Observação Clínica', 20); -- só precisaria de 3 unidades


-- atendimentos
INSERT INTO atendimento (id_atendimento, id_paciente, id_residente, id_preceptor, data_hora, duracao_minutos)
VALUES
    (10, 1, 3, 1, '2026-06-01 08:30:00', 30),
    (20, 2, 2, 1, '2026-06-01 09:15:00', 45),
    (30, 3, 5, 2, '2026-06-02 10:00:00', 20),
    (40, 4, 1, 2, '2026-06-02 11:30:00', 60),
    (50, 5, 3, 3, '2026-06-03 08:00:00', 25),
    (60, 6, 4, 1, '2026-06-03 14:20:00', 40),
    (70, 7, 2, 3, '2026-06-04 09:45:00', 35),
    (80, 8, 1, 2, '2026-06-04 13:10:00', 15),
    (90, 9, 4, 3, '2026-06-05 10:30:00', 50),
    (11, 10, 5, 1, '2026-06-05 16:00:00', 30);

-- procedimentos

-- procedimentos realizados
INSERT INTO procedimento_realizado (id_atendimento, id_procedimento, quantidade, tempo_real_minutos, observacao)
VALUES
    (1, 1, 1, 25, 'Procedimento sem intercorrências'),
    (2, 2, 2, 40, 'Paciente colaborativo'),
    (3, 1, 1, 18, NULL),
    (4, 3, 1, 55, 'Necessário auxílio do preceptor'),
    (5, 2, 1, 20, 'Realizado rapidamente'),
    (6, 4, 3, 35, 'Repetido devido a erro inicial'),
    (7, 1, 1, 30, NULL),
    (8, 5, 1, 12, 'Procedimento simples'),
    (9, 3, 2, 45, 'Leve atraso no início'),
    (10, 2, 1, 28, NULL);

-- alergias
INSERT INTO alergia(id_alergia, id_pessoa, tipo_alergia)
VALUES
    (10, 1, 'Ovo'),
    (20, 2, 'Poeira'),
    (30, 3, 'Dipirona'),
    (40, 4, 'Água'),
    (50, 5, 'Poeira');

