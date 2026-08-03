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
│   ├── DER_Completo.pdf
│   └── modelagem.pdf
│
├── sql/
│   ├── schema.sql
│   ├── CRUD.sql
│   ├── analytics.sql
│   ├── views.sql
│   ├── triggers.sql
│   ├── procedures.sql
│   └── test_cases.sql
│
├── orm/
│   ├── database.py
│   ├── models.py
│   ├── CRUD.py
│   ├── adv_queries.py
│   ├── procedures.py
│   ├── triggers.py
│   ├── views.py
│   ├── concurrency.py
│   ├── main.py
│   ├── test_cases.py
│   └── .env
│
├── ui/
│   ├── app.py
│   ├── routes/
│   │   ├── home.py
│   │   ├── pacientes.py
│   │   ├── profissionais.py
│   │   ├── atendimentos.py
│   │   ├── plantoes.py
│   │   ├── procedimentos.py
│   │   ├── unidades.py
│   │   ├── internacoes.py
│   │   ├── analytics.py
│   │   └── views.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── pacientes.html
│   │   ├── profissionais.html
│   │   ├── atendimentos.html
│   │   ├── plantoes.html
│   │   ├── procedimentos.html
│   │   ├── unidades.html
│   │   ├── internacoes.html
│   │   ├── analytics.html
│   │   └── views.html
│   └── static/
│       ├── css/style.css
│       └── js/main.js
│
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```
