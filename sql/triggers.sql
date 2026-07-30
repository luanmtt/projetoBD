/*


triggers.sql:

Esse arquivo contêm os triggers, as ações condicionais que atuam sobre algumas
regras de negócio identificadas pela requisição do projeto.
Esses são:


    • trg_check_sobreposicao_escala: BEFORE INSERT/UPDATE na tabela ESCALA. 
        → Impede que um mesmo residente seja escalado no mesmo dia/turno em duas unidades diferentes.

    • trg_audita_atendimento: AFTER INSERT/UPDATE/DELETE em ATENDIMENTO. 
        → Registra em uma tabela AUDITORIA_ATENDIMENTO (id_auditoria, id_atendimento, operacao, usuario, 
                                                        data_hora, dados_antigos (JSON), dados_novos (JSON)).

    • trg_atualiza_media_procedimentos: AFTER INSERT em PROCEDIMENTO_REALIZADO. 
        → Atualiza uma coluna media_tempo_procedimento na tabela PROCEDIMENTO (média do tempo_real_minutos daquele procedimento 
                                                                               em todos os atendimentos).


*/


-- ─────────────────────────────────────────────────────────────────────────────────────────────────
-- trg_check_sobreposicao_escala


-- função do trigger
CREATE OR REPLACE FUNCTION sobreposicao_escala()
RETURNS TRIGGER AS $$ 

DECLARE
    verif_turno VARCHAR(10);
    verif_dia_semana DATE;
    verif_id_unidade INTEGER;
    nome_unidade VARCHAR(50);

BEGIN

    SELECT turno, dia_semana, id_unidade INTO v_turno, v_dia_semana, v_unidade
    FROM plantao
    WHERE id_plantao = NEW.id_plantao;

    IF EXISTS(

        SELECT 1
        FROM escala es
        INNER JOIN plantao pl ON es.id_plantao = pl.id_plantao
        WHERE es.id_residente = NEW.id_residente
        AND pl.turno = verif_turno
        AND pl.dia_semana = verif_dia_semana
        AND pl.id_unidade <> verif_id_unidade -- <> em sql !=         
        

    ) THEN 

    RAISE EXCEPTION 'Residente % já está escalado no dia % turno % em outra unidade % ',
            NEW.id_residente, v_dia_semana, v_turno; 
            /*,
                -- se quiser pegar o nome da unidade

                SELECT u.nome_unidade
                FROM escala es
                INNER JOIN plantao pl ON es.id_plantao = pl.id_plantao
                INNER JOIN unidade u ON pl.id_unidade = u.id_unidade
                WHERE es.id_residente = NEW.id_residente
                   AND pl.turno = v_turno
                   AND pl.dia_semana = v_dia_semana
                   AND pl.id_unidade <> v_unidade
                LIMIT 1
            );
            */
    END IF;

RETURN NEW;

END;
$$ 
LANGUAGE plpgsql;


CREATE TRIGGER trg_check_sobreposicao_escala
BEFORE INSERT OR UPDATE ON escala
FOR EACH ROW
EXECUTE PROCEDURE sobreposicao_escala();


-- ─────────────────────────────────────────────────────────────────────────────────────────────────
-- trg_audita_atendimento


-- função do trigger
CREATE OR REPLACE FUNCTION funcao_auditoria_atendimento()
RETURNS TRIGGER AS $$

BEGIN 
    
    IF TG_OP = 'INSERT' THEN 

        INSERT INTO auditoria_atendimento 
        (id_atendimento, data_hora, operacao, usuario, dados_novos, dados_antigos)
        VALUES
        (NEW.id_atendimento, now(), TG_OP, current_user, row_to_json(NEW), NULL);

        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN 

        INSERT INTO auditoria_atendimento 
        (id_atendimento, data_hora, operacao, usuario, dados_novos, dados_antigos)
        VALUES
        (NEW.id_atendimento, now(), TG_OP, current_user, row_to_json(NEW), row_to_json(OLD));
        
        RETURN NEW;

    ELSIF TG_OP = 'DELETE'
    
        THEN

        INSERT INTO auditoria_atendimento 
        (id_atendimento, data_hora, operacao, usuario, dados_novos, dados_antigos)
        VALUES
        (OLD.id_atendimento, now(), TG_OP, current_user, NULL, row_to_json(OLD));

        RETURN OLD;
        
    END IF;


END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER trg_audita_atendimento
AFTER INSERT OR UPDATE OR DELETE ON atendimento
FOR EACH ROW
EXECUTE PROCEDURE funcao_auditoria_atendimento();


-- ─────────────────────────────────────────────────────────────────────────────────────────────────
-- trg_atualiza_media_procedimentos


-- função do trigger
CREATE OR REPLACE FUNCTION atualiza_media()
RETURN TRIGGER AS $$
DECLARE
    media_antiga  NUMERIC;
    media_nova    NUMERIC;
    nome_proc     VARCHAR(100);

BEGIN
        
    SELECT media_tempo_procedimento, nome
    INTO media_antiga, nome_proc
    FROM procedimento
    WHERE id_procedimento = NEW.id_procedimento;
    
    SELECT AVG(tempo_real_minutos)
    INTO media_nova
    FROM procedimento_realizado
    WHERE id_procedimento = NEW.id_procedimento;

    RAISE NOTICE 'A média do procedimento "%" passou de %min para %min', 
    nome_proc, media_nova, media_antiga;

RETURN NULL;

END
$$
LANGUAGE plpgsql;


CREATE TRIGGER trg_atualiza_media_procedimentos
AFTER INSERT ON procedimento_realizado
FOR EACH ROW
EXECUTE PROCEDURE atualiza_media();


-- ─────────────────────────────────────────────────────────────────────────────────────────────────
-- logs


-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
