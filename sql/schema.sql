/*

schema.sql:

Esse arquivo será aquele no qual as tabelas serão CRIADAS. Ou seja, CREATE TABLES com tipagem dos atributos,
definições de quais atributos serão chave primária, candidata, estrangeira; implementação de constraits; entre outros.
A estrutura das tabelas, chaves, atributos seguem o Diagrama Entidade-Relacionamento feito na Etapa 1 - Modelagem.
O arquivo de modelagem está na root do projeto como Modelagem.pdf.


*/

DROP TABLE IF EXISTS escala CASCADE;
DROP TABLE IF EXISTS plantao CASCADE;
DROP TABLE IF EXISTS procedimento_realizado CASCADE;
DROP TABLE IF EXISTS procedimento CASCADE;
DROP TABLE IF EXISTS nivel_risco CASCADE;
DROP TABLE IF EXISTS atendimento CASCADE;
DROP TABLE IF EXISTS alergia CASCADE;
DROP TABLE IF EXISTS unidade CASCADE;
DROP TABLE IF EXISTS residente CASCADE;
DROP TABLE IF EXISTS preceptor CASCADE;
DROP TABLE IF EXISTS profissional CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS pessoa CASCADE;

-- CRIAÇÃO DE TABELAS

CREATE TABLE pessoa(
	id_pessoa SERIAL PRIMARY KEY,
	nome VARCHAR(50) NOT NULL, 								-- um nome não pode ser vazio.
	cpf VARCHAR(14) UNIQUE NOT NULL DEFAULT '000-000-000.00', -- um cpf não pode ser vazio.
	data_nascimento VARCHAR(10) NOT NULL DEFAULT '00/00/0000',	-- uma data de nascimento não pode ser vazia.
	is_flamengo BOOLEAN,
	telefone VARCHAR(16) UNIQUE NOT NULL DEFAULT '00(00)00000-0000'
);


CREATE TABLE paciente(
	id_paciente INTEGER PRIMARY KEY,
	num_convenio VARCHAR(20) UNIQUE NOT NULL DEFAULT 'NOMECONVENIO-00000',
	grupo_sanguineo VARCHAR(3) NOT NULL,

	CONSTRAINT fk_paciente
		FOREIGN KEY (id_paciente)
		REFERENCES pessoa(id_pessoa)
		ON DELETE CASCADE
);


CREATE TABLE profissional(
	id_profissional INTEGER PRIMARY KEY,
	crm VARCHAR(8) UNIQUE NOT NULL DEFAULT 'AA-000000',
	data_admissao VARCHAR(10) NOT NULL DEFAULT '00/00/0000',
	especialidade VARCHAR(20) NOT NULL,

	CONSTRAINT fk_profissional
		FOREIGN KEY (id_profissional)
		REFERENCES pessoa(id_pessoa)
		ON DELETE CASCADE
);


CREATE TABLE preceptor(
	id_preceptor INTEGER PRIMARY KEY,
	titulacao VARCHAR(20) NOT NULL,

	CONSTRAINT fk_preceptor
		FOREIGN KEY (id_preceptor)
		REFERENCES profissional(id_profissional)

);


CREATE TABLE residente(
	id_residente INTEGER PRIMARY KEY,
	ano_residencia INTEGER NOT NULL,

	CONSTRAINT fk_residente
		FOREIGN KEY (id_residente)
		REFERENCES profissional(id_profissional)
		ON DELETE CASCADE

);

CREATE TABLE alergia(
	id_alergia SERIAL PRIMARY KEY,
	id_pessoa INT NOT NULL,
	tipo_alergia VARCHAR(30) NOT NULL,

	CONSTRAINT fk_alergias
		FOREIGN KEY (id_pessoa)
		REFERENCES pessoa(id_pessoa)
		ON DELETE CASCADE,

	CONSTRAINT uq_pessoa
		UNIQUE (id_pessoa, tipo_alergia)
);


CREATE TABLE unidade(
	id_unidade SERIAL PRIMARY KEY NOT NULL,
	nome VARCHAR(20) NOT NULL,
	tipo VARCHAR(50) NOT NULL,
	capacidade_leitos INTEGER NOT NULL CHECK (capacidade_leitos >= 0)
);


CREATE TABLE atendimento(
	id_atendimento SERIAL PRIMARY KEY NOT NULL,
	id_paciente INTEGER NOT NULL,
	id_residente INTEGER NOT NULL,
	id_preceptor INTEGER NOT NULL,
	data_hora TIMESTAMP NOT NULL,
	duracao_minutos NUMERIC(4,2) NOT NULL CHECK (duracao_minutos >= 0) CHECK (duracao_minutos < 1000),

	CONSTRAINT fk_atendimento_paciente
        FOREIGN KEY (id_paciente)
        REFERENCES paciente(id_paciente)
		ON DELETE CASCADE,

    CONSTRAINT fk_atendimento_residente
        FOREIGN KEY (id_residente)
        REFERENCES residente(id_residente)
		ON DELETE CASCADE,

    CONSTRAINT fk_atendimento_preceptor
        FOREIGN KEY (id_preceptor)
        REFERENCES preceptor(id_preceptor)
        ON DELETE CASCADE
);

CREATE TABLE nivel_risco(
    id_nivel_risco SERIAL PRIMARY KEY,
    nivel VARCHAR(10) UNIQUE NOT NULL CHECK (nivel IN ('BAIXO','MEDIO','ALTO'))
);

CREATE TABLE procedimento(
	id_procedimento SERIAL PRIMARY KEY NOT NULL,
	id_nivel_risco INTEGER NOT NULL,
	codigo VARCHAR(9) NOT NULL DEFAULT 'PROC-0000',
	nome VARCHAR(50) NOT NULL,
	tempo_medio_minutos NUMERIC(4,2) NOT NULL CHECK (tempo_medio_minutos >= 0) CHECK (tempo_medio_minutos < 1000),

	CONSTRAINT fk_nivel_risco
        FOREIGN KEY (id_nivel_risco)
        REFERENCES nivel_risco(id_nivel_risco)
        ON DELETE cascade
);

CREATE TABLE procedimento_realizado(
	id_atendimento INTEGER NOT NULL,
	id_procedimento INTEGER NOT NULL,
	quantidade INTEGER NOT NULL,
	observacao TEXT,
	tempo_real_minutos NUMERIC(4,2) NOT NULL CHECK (tempo_real_minutos >= 0) CHECK(tempo_real_minutos < 1000),
    faturamento_processado BOOLEAN DEFAULT FALSE,

	-- pk composta
	CONSTRAINT pk_procedimento_realizado
        PRIMARY KEY (id_atendimento, id_procedimento),

	CONSTRAINT fk_atendimento
        FOREIGN KEY (id_atendimento)
        REFERENCES atendimento(id_atendimento)
        ON DELETE CASCADE,

    CONSTRAINT fk_procedimento
        FOREIGN KEY (id_procedimento)
        REFERENCES procedimento(id_procedimento)
        ON DELETE CASCADE
);


CREATE TABLE plantao(

	id_plantao SERIAL PRIMARY KEY NOT NULL,
	id_preceptor INTEGER NOT NULL,
	id_unidade INTEGER NOT NULL,
	dia_semana DATE NOT NULL,
	turno VARCHAR(10) NOT NULL CHECK (turno IN ('manhã', 'tarde', 'noite')),

	-- unique id_unidade, dia_semana, turno. tupla única, evita repetição de um turno no mesmo dia.
	CONSTRAINT unq_plantao
		UNIQUE(id_unidade, dia_semana, turno),

	CONSTRAINT fk_unidade
        FOREIGN KEY (id_unidade)
        REFERENCES unidade(id_unidade)
        ON DELETE CASCADE,

    CONSTRAINT fk_preceptor
        FOREIGN KEY (id_preceptor)
        REFERENCES preceptor(id_preceptor)
        ON DELETE CASCADE
);


CREATE TABLE escala(
	id_escala SERIAL PRIMARY KEY NOT NULL,
	id_plantao INTEGER NOT NULL,
	id_residente INTEGER NOT NULL,

	--unique id_plantao, id_residente. tupla única, evita escalas repetidas.
	CONSTRAINT unq_escala
		UNIQUE(id_plantao, id_residente),

	CONSTRAINT fk_plantao
        FOREIGN KEY (id_plantao)
        REFERENCES plantao(id_plantao)
        ON DELETE CASCADE,

    CONSTRAINT fk_residente
        FOREIGN KEY (id_residente)
        REFERENCES residente(id_residente)
        ON DELETE CASCADE
);


-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
