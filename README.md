# Projeto de Banco de Dados - Sistema de Gestão Hospitalar

Esse repositório contém os códigos relativos ao projeto da disciplina de Banco de Dados, ministrada pelo professor Marcelo Iury. O projeto consiste em "um sistema hospitalar para gerenciar atendimentos, profissionais, pacientes, procedimentos, internações e escalas de plantão".

O projeto é feito em grupo, sendo o nosso grupo composto por: Luan Motta e Costa, Lucas Schettini de Oliveira, Akemi Almirante de Brito e Carlos Andrei Cicero Sousa Maia.

O projeto é dividido em duas etapas:

* **Etapa 1:** Implementação de scripts base usando `.sql` puro, sem o uso de ORM.
* **Etapa 2:** Implementação de funções e regras de negócio mais complexas usando ORM.

## Objetivos de Aprendizagem

1. Modelagem conceitual, lógica e física (DER → MR → SQL)
2. Normalização até 3FN/BCNF
3. SQL avançado (junções, subconsultas, agregações, views)
4. Triggers e stored procedures
5. Uso de ORM (SQLAlchemy, Prisma, Hibernate, Entity Framework, ou similar)
6. Controle de transações e integridade referencial

---
## Instalação e Execução

1. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

2. Edite o arquivo `.env` com os dados de conexão do seu banco PostgreSQL:

```env
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nome_do_banco
```

3. Certifique-se de que o PostgreSQL esteja em execução e que o banco de dados já tenha sido criado.

4. Na pasta principal do projeto, execute:

```bash
python run.py
```

No Windows, também pode ser utilizado:

```bash
py run.py
```

5. Com o servidor iniciado, acesse no navegador:

```text
http://127.0.0.1:5000
```

Para encerrar a aplicação, pressione:

```text
Ctrl + C
```

## Estrutura do Repositório

```text
projetoBD
│
├── docs/
│   ├── DER_Completo.pdf    # Diagrama Entidade-Relacionamento completo do projeto
│   └── modelagem.pdf       # Documento de modelagem conceitual, lógica e física
│
├── sql/
│   ├── schema.sql          # Definição do esquema do banco de dados (CREATE TABLEs, constraints, chaves)
│   ├── CRUD.sql            # Operações de Create, Read, Update e Delete sobre as tabelas
│   ├── analytics.sql       # Consultas analíticas (rankings, agregações, estatísticas)
│   ├── views.sql           # Criação de Views (rankings procedimento, atendimentos, residentes) 
│   ├── triggers.sql        # Criação de triggers para auditoria, checagem de regra de negócio e estatísticas
│   └── test_cases.sql      # Dados de teste para popular o banco (pessoas, atendimentos, procedimentos, etc.)
│
├── orm/                    # Camada de acesso a dados via SQLAlchemy
│   ├── database.py         # Conexão com o banco (engine, sessão)
│   ├── models.py           # Mapeamento objeto-relacional: classes Python ↔ tabelas
│   ├── CRUD.py             # Operações de Create, Read, Update e Delete via ORM
│   ├── consultations.py    # Consultas analíticas via ORM
│   ├── main.py             # Script principal de execução do backend
│   ├── test_cases.py       # Dados de teste em Python (equivalente ao test_cases.sql)
│   └── .env                # Deve ser criado para acesso ao banco
│
├── ui/                     # Interface web com Flask + Jinja2
│   ├── app.py              # Fábrica da aplicação Flask
│   ├── routes/             # Rotas HTTP organizadas por recurso (blueprints)
│   │   ├── home.py
│   │   ├── pacientes.py
│   │   ├── profissionais.py
│   │   ├── atendimentos.py
│   │   └── plantoes.py
│   ├── templates/          # Templates HTML com Jinja2 (base + páginas)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── pacientes.html
│   │   ├── profissionais.html
│   │   ├── atendimentos.html
│   │   └── plantoes.html
│   └── static/             # Arquivos estáticos (CSS, JS)
│       ├── css/style.css
│       └── js/main.js
│
├── run.py                  # Ponto de entrada da aplicação (`python run.py`)
├── requirements.txt        # Dependências Python (Flask, SQLAlchemy, psycopg2)
├── .gitignore              # Arquivos e diretórios ignorados pelo Git
└── README.md               # o que estás lendo!
```
