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

### 1. Windows

1. Acesse a página de download do PostgreSQL e clique em "Download the installer" (mantido pela EnterpriseDB).
2. Baixe a versão mais recente para Windows x86-64.
3. Execute o instalador baixado.
4. Siga o assistente de instalação:
   * **Componentes:** Deixe marcados o PostgreSQL Server, pgAdmin 4 (interface gráfica) e Command Line Tools.
   * **Senha:** Ele pedirá para criar uma senha para o superusuário padrão (chamado `postgres`). Não esqueça essa senha.
   * **Porta:** Deixe a porta padrão (`5432`).

**Como rodar e acessar:**

O PostgreSQL já estará rodando como um serviço do Windows em segundo plano.

* **Via Interface Gráfica:** Abra o Menu Iniciar, procure por `pgAdmin 4`, abra o programa, digite a senha que você criou e conecte-se ao seu servidor local.
* **Via Terminal:** Abra o Menu Iniciar, procure por `SQL Shell (psql)`. Pressione "Enter" para aceitar os valores padrão até ele pedir a sua senha. Digite a senha (ela não aparecerá na tela) e dê "Enter". Siga para o passo de criação do banco descrito na seção do Linux (Passos 4 a 6).

### 2. Linux (Debian/Ubuntu)

1. Instalar o PostgreSQL para o seu ambiente:
   ```bash
   sudo apt install postgresql postgresql-contrib 
   ```

2. Ativar o serviço do PostgreSQL:
   ```bash
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

3. Abrir o terminal do banco de dados:
   ```bash
   sudo psql -U postgres
   ```

4. Criar o banco de dados:
   ```sql
   DROP DATABASE IF EXISTS hospitalbd;
   CREATE DATABASE hospitalbd;
   ```

5. Conectar no banco criado:
   ```sql
   \c hospitalbd
   ```

6. Rodar o esquema (tabelas):
   ```sql
   \i sql/schema.sql
   ```

7. Popular com dados de teste:
   ```sql
   \i sql/test_cases.sql 
   ```

8. Usar das consultas/operações presentes em `sql/CRUD.sql` e `sql/analytics.sql`.

### 3. macOS

**Como instalar:**

A maneira mais recomendada e prática no macOS é utilizando o Homebrew (gerenciador de pacotes). Abra o terminal e execute:
```bash
brew install postgresql
```

1. Inicie o serviço do PostgreSQL em segundo plano:
   ```bash
   brew services start postgresql
   ```

2. Abra o terminal interativo do banco de dados:
   ```bash
   psql postgres
   ```

3. Criar o banco de dados:
   ```sql
   DROP DATABASE IF EXISTS hospitalbd;
   CREATE DATABASE hospitalbd;
   ```

4. Conectar no banco criado:
   ```sql
   \c hospitalbd
   ```

5. Rodar o esquema (tabelas):
   ```sql
   \i sql/schema.sql
   ```

6. Popular com dados de teste:
   ```sql
   \i sql/test_cases.sql 
   ```

7. Usar das consultas/operações presentes em `sql/CRUD.sql` e `sql/analytics.sql`.

---

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
