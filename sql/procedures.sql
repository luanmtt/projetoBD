
--procedure 1: registra atendimento completo

CREATE OR REPLACE PROCEDURE sp_registrar_atendimento_completo(
    p_id_paciente INTEGER,
    p_id_residente INTEGER,
    p_id_preceptor INTEGER,
    p_id_unidade INTEGER,
    p_data_hora TIMESTAMP,
    p_duracao_minutos NUMERIC(4,2),
    p_procedimentos JSONB
)

LANGUAGE plpgsql
AS $$
DECLARE
    novo_id_atendimento INTEGER;
    procedimento_json JSONB;
    verif_id_procedimento INTEGER;
    verif_quantidade INTEGER;
    verif_observacao TEXT;
    verif_data_hora_inicio TIMESTAMP;
    verif_tempo_real NUMERIC(4,2);
BEGIN

    -- verifica se o paciente existe
    IF NOT EXISTS (
        SELECT 1
        FROM paciente
        WHERE id_paciente = p_id_paciente
    ) THEN
        RAISE EXCEPTION 'Paciente não existe';
    END IF;

    -- verifica se o residente existe
    IF NOT EXISTS (
        SELECT 1
        FROM residente
        WHERE id_residente = p_id_residente
    ) THEN
        RAISE EXCEPTION 'Residente não existe';
    END IF;

    -- verifica se o preceptor existe
    IF NOT EXISTS (
        SELECT 1
        FROM preceptor
        WHERE id_preceptor = p_id_preceptor
    ) THEN
        RAISE EXCEPTION 'Preceptor não existe';
    END IF;

    -- verifica se a unidade existe
    IF NOT EXISTS (
        SELECT 1
        FROM unidade
        WHERE id_unidade = p_id_unidade
    ) THEN
        RAISE EXCEPTION 'Unidade não existe';
    END IF;

    -- verifica se a duração é válida
    IF p_duracao_minutos IS NULL
       OR p_duracao_minutos < 0 THEN
        RAISE EXCEPTION 'Duração do atendimento inválida';
    END IF;

    -- verifica se o tipo de arquivo é um JSON
    IF p_procedimentos IS NULL
       OR jsonb_typeof(p_procedimentos) <> 'array' THEN
        RAISE EXCEPTION 'A lista de procedimentos deve ser um array JSON';
    END IF;


    -- verifica se a lista de procedimentos está vazia
    IF jsonb_array_length(p_procedimentos) = 0 THEN
        RAISE EXCEPTION 'O atendimento deve possuir ao menos um procedimento';
    END IF;

    -- insere o atendimento
    INSERT INTO atendimento (
        id_paciente,
        id_residente,
        id_preceptor,
        id_unidade,
        data_hora,
        duracao_minutos
    )
    VALUES (
        p_id_paciente,
        p_id_residente,
        p_id_preceptor,
        p_id_unidade,
        p_data_hora,
        p_duracao_minutos
    )
    RETURNING id_atendimento
    INTO novo_id_atendimento;

    -- percorre procedimento
    FOR procedimento_json IN
        SELECT *
        FROM jsonb_array_elements(p_procedimentos)
    LOOP

        -- guarda os dados do procedimento em variáveis
        verif_id_procedimento :=
            (procedimento_json ->> 'id_procedimento')::INTEGER;
        verif_quantidade :=
            (procedimento_json ->> 'quantidade')::INTEGER;
        verif_observacao :=
            procedimento_json ->> 'observacao';
        verif_data_hora_inicio :=
            (procedimento_json ->> 'data_hora_inicio')::TIMESTAMP;
        verif_tempo_real :=
            (procedimento_json ->> 'tempo_real_minutos')::NUMERIC;

        -- verifica se o procedimento existe
        IF NOT EXISTS (
            SELECT 1
            FROM procedimento
            WHERE id_procedimento = verif_id_procedimento
        ) THEN
            RAISE EXCEPTION
                'Procedimento % não existe', verif_id_procedimento;
        END IF;

        -- verificar se a quantidade é válida
        IF verif_quantidade IS NULL
           OR verif_quantidade <= 0 THEN
            RAISE EXCEPTION 'Quantidade inválida para o procedimento %', verif_id_procedimento;
        END IF;

        -- verifica se o horário de início foi informado
        IF verif_data_hora_inicio IS NULL THEN
            RAISE EXCEPTION 'Horário de início não informado para o procedimento %', verif_id_procedimento;
        END IF;

        -- impede procedimento antes do início do atendimento
        IF verif_data_hora_inicio < p_data_hora THEN
            RAISE EXCEPTION 'O procedimento % não pode começar antes do atendimento', verif_id_procedimento;
        END IF;

        -- verifica se o tempo real é válido
        IF verif_tempo_real IS NULL
           OR verif_tempo_real < 0 THEN

            RAISE EXCEPTION
                'Tempo real inválido para o procedimento %', verif_id_procedimento;
        END IF;

        -- insere o procedimento realizado
        INSERT INTO procedimento_realizado (
            id_atendimento,
            id_procedimento,
            quantidade,
            observacao,
            data_hora_inicio,
            tempo_real_minutos,
            faturamento_processado
        )
        VALUES (
            novo_id_atendimento,
            verif_id_procedimento,
            verif_quantidade,
            verif_observacao,
            verif_data_hora_inicio,
            verif_tempo_real,
            FALSE
        );

    END LOOP;


    RAISE NOTICE 'Atendimento % cadastrado com sucesso', novo_id_atendimento;
END;
$$;


-- procedure 2: calcula o tempo médio de espera por unidade

CREATE OR REPLACE PROCEDURE sp_calcular_tempo_medio_espera()
LANGUAGE plpgsql
AS $$
BEGIN

    -- apaga o resultado anterior, caso exista
    DROP TABLE IF EXISTS resultado_tempo_medio_espera;

    -- cria uma tabela temporária com o resultado
    CREATE TEMP TABLE resultado_tempo_medio_espera AS
    SELECT
        u.id_unidade,
        u.nome AS nome_unidade,

        ROUND(
            AVG(
                EXTRACT(
                    EPOCH FROM (
                        primeiro_procedimento.data_hora_inicio
                        - a.data_hora
                    )
                ) / 60.0
            ),
            2
        ) AS tempo_medio_espera_minutos

    FROM atendimento a
    JOIN unidade u
        ON u.id_unidade = a.id_unidade
    JOIN (
        -- encontrar o primeiro procedimento de cada atendimento
        SELECT
            id_atendimento,
            MIN(data_hora_inicio) AS data_hora_inicio
        FROM procedimento_realizado
        GROUP BY id_atendimento
    ) primeiro_procedimento
        ON primeiro_procedimento.id_atendimento =
           a.id_atendimento
    GROUP BY
        u.id_unidade,
        u.nome
    ORDER BY
        u.id_unidade;
    RAISE NOTICE 'Tempo médio de espera calculado com sucesso';

END;
$$;

-- procedure 3: reajusta escala de um residente

CREATE OR REPLACE PROCEDURE sp_reajustar_escala(
    p_id_residente INTEGER,
    p_dia_antigo DATE,
    p_turno_antigo VARCHAR(10),
    p_dia_novo DATE,
    p_turno_novo VARCHAR(10)
)
LANGUAGE plpgsql
AS $$
DECLARE
    escala_atual RECORD;
    novo_id_plantao INTEGER;
    quantidade_alterada INTEGER := 0;

BEGIN

    -- verifica se o residente existe
    IF NOT EXISTS (
        SELECT 1
        FROM residente
        WHERE id_residente = p_id_residente
    ) THEN

        RAISE EXCEPTION 'Residente não existe';
    END IF;

    -- verifica se o turno antigo é válido
    IF p_turno_antigo NOT IN (
        'manhã',
        'tarde',
        'noite'
    ) THEN
        RAISE EXCEPTION 'Turno antigo inválido';
    END IF;

    -- verifica se o turno novo é válido
    IF p_turno_novo NOT IN (
        'manhã',
        'tarde',
        'noite'
    ) THEN
        RAISE EXCEPTION 'Turno novo inválido';

    END IF;


    -- verifica se o residente possui escala no dia e turno antigos
    IF NOT EXISTS (
        SELECT 1

        FROM escala e

        JOIN plantao p
            ON p.id_plantao = e.id_plantao

        WHERE e.id_residente = p_id_residente
          AND p.dia_semana = p_dia_antigo
          AND p.turno = p_turno_antigo
    ) THEN

        RAISE EXCEPTION 'O residente não possui escala no dia e turno informados';
    END IF;

    -- verifica se o residente já possui escala no novo dia e turno
    IF EXISTS (
        SELECT 1
        FROM escala e
        JOIN plantao p
            ON p.id_plantao = e.id_plantao
        WHERE e.id_residente = p_id_residente
          AND p.dia_semana = p_dia_novo
          AND p.turno = p_turno_novo
    ) THEN
        RAISE EXCEPTION 'O residente já possui escala no novo dia e turno';
    END IF;

    -- percorre todas as escalas do residente no dia e turno antigos
    FOR escala_atual IN
        SELECT
            e.id_escala,
            p.id_unidade,
            p.id_preceptor
        FROM escala e
        JOIN plantao p
            ON p.id_plantao = e.id_plantao
        WHERE e.id_residente = p_id_residente
          AND p.dia_semana = p_dia_antigo
          AND p.turno = p_turno_antigo
    LOOP
        novo_id_plantao := NULL;

        -- procura um plantão existente na mesma unidade, no novo dia e turno
        SELECT id_plantao
        INTO novo_id_plantao
        FROM plantao
        WHERE id_unidade = escala_atual.id_unidade
          AND dia_semana = p_dia_novo
          AND turno = p_turno_novo;

        -- cria um novo plantão caso ele ainda não exista
        IF novo_id_plantao IS NULL THEN

            INSERT INTO plantao (
                id_preceptor,
                id_unidade,
                dia_semana,
                turno
            )
            VALUES (
                escala_atual.id_preceptor,
                escala_atual.id_unidade,
                p_dia_novo,
                p_turno_novo
            )
            RETURNING id_plantao
            INTO novo_id_plantao;
        END IF;

        -- muda a escala para o novo plantão
        UPDATE escala
        SET id_plantao = novo_id_plantao
        WHERE id_escala = escala_atual.id_escala;
        quantidade_alterada :=
            quantidade_alterada + 1;

    END LOOP;
    RAISE NOTICE
        '% escala(s) foram alteradas',
        quantidade_alterada;
END;
$$;