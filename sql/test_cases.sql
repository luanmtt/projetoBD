/*

test_cases.sql:

Esse arquivo contêm as entries de teste que o sistema demanda para funcionar. assim como especificado
no projeto, serão adicionados 5 pacientes, 5 residentes, 5 preceptores, 3 unidades, 10 atendimentos e 10 procedimentos realizados

*/

-- add Pessoas

INSERT INTO pessoa(nome, cpf, data_nascimento, is_flamengo, telefone )
VALUES
	('Luan Motta', '210.113.954-60', '01/10/44', FALSE, '55(81)95509-5100'),
    ('Lucas Schettini', '196.685.636-70', '27/05/28', TRUE, '55(71)93284-2315'),
    ('Akemi Almirante', '742.807.130-58', '10/04/52', FALSE, '55(11)91853-9648'),
    ('Andrei Maia', '852.159.098-30', '20/12/53', TRUE, '55(71)93522-5986'),
    ('Marlon Neto', '837.851.729-77', '26/08/16', TRUE, '55(51)97295-3461'),
    ('Marcelo Iury', '400.878.351-11', '16/09/22', TRUE, '55(71)95858-7524'),
    ('Neymar Jr', '461.301.397-10', '03/04/96', FALSE, '55(41)95727-5013'),
    ('Michael Scott', '634.706.010-18', '12/01/73', TRUE, '55(85)96173-5506'),
    ('Clark Kent', '826.526.064-04', '02/11/43', TRUE, '55(91)97894-7684'),
    ('Bob Jackson', '156.786.184-88', '12/12/80', FALSE, '55(41)94083-6938'),
    ('Alice Kennedy', '130.776.889-76', '09/11/29', TRUE, '55(51)98561-9000');
	('Drauzio Varella', '085.784.728-33', '09/11/11', FALSE, '55(85)92621-7758'),
    ('Oswaldo Cruz', '491.691.164-83', '03/05/29', FALSE, '55(85)97973-7039'),
    ('Antônio de Salles', '981.246.846-10', '14/01/92', FALSE, '55(71)93021-1378'),
    ('Angelita Habr-Gama ', '937.898.585-55', '24/11/23', FALSE, '55(71)93537-1108');

-- especialização de Pacientes

-- especialização de Profissionais

-- especialização de Preceptores

-- especialização de Residentes


-- unidades
INSERT INTO unidade(nome, tipo, capacidade_leitos)
VALUES
	('Trauminha','Emergência Ortotraumatológica',55),
	('Oncologia','Tratamento de Câncer',18),
	('Centro Cirúrgico','Cirurgia',40),
	('Centro de Observação', 'Observação Clínica', 20);


-- atendimentos
INSERT INTO atendimento (id_paciente, id_residente, id_preceptor, data_hora, duracao_minutos)
VALUES
    (1, 3, 1, '2026-06-01 08:30:00', 30),
    (2, 2, 1, '2026-06-01 09:15:00', 45),
    (3, 5, 2, '2026-06-02 10:00:00', 20),
    (4, 1, 2, '2026-06-02 11:30:00', 60),
    (5, 3, 3, '2026-06-03 08:00:00', 25),
    (6, 4, 1, '2026-06-03 14:20:00', 40),
    (7, 2, 3, '2026-06-04 09:45:00', 35),
    (8, 1, 2, '2026-06-04 13:10:00', 15),
    (9, 4, 3, '2026-06-05 10:30:00', 50),
    (10, 5, 1, '2026-06-05 16:00:00', 30);


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




