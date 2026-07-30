# seed.py
from datetime import date, datetime
from decimal import Decimal
from database import SessionLocal, engine, Base
from models import (
    Paciente, Preceptor, Residente, Unidade, Atendimento, 
    NivelRisco, Procedimento, ProcedimentoRealizado, Alergia
)

def popular_banco():
    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as session:
        if session.query(Paciente).first():
            print("O banco já possui dados populados.")
            return
        # 1. Pacientes 
        pacientes = [
            Paciente(
                id_pessoa=1, id_paciente=1, nome='Luan Motta', cpf='210.113.954-60',
                data_nascimento=date(1944, 10, 1), is_flamengo=False, telefone='55(81)95509-5100',
                endereco='Rua da Mãe Joana, 404', num_convenio='UNIMED-88213', grupo_sanguineo='O+'
            ),
            Paciente(
                id_pessoa=2, id_paciente=2, nome='Lucas Schettini', cpf='196.685.636-70',
                data_nascimento=date(1928, 5, 27), is_flamengo=True, telefone='55(71)93284-2315',
                endereco='Rua dos Bobos, 0', num_convenio='BRADESCO-44210', grupo_sanguineo='A-'
            ),
            Paciente(
                id_pessoa=3, id_paciente=3, nome='Akemi Almirante', cpf='742.807.130-58',
                data_nascimento=date(1952, 4, 10), is_flamengo=False, telefone='55(11)91853-9648',
                endereco='Manaíra', num_convenio='AMIL-90911', grupo_sanguineo='B+'
            ),
            Paciente(
                id_pessoa=4, id_paciente=4, nome='Andrei Maia', cpf='852.159.098-30',
                data_nascimento=date(1953, 12, 20), is_flamengo=True, telefone='55(71)93522-5986',
                endereco='Aguiar', num_convenio='SULAMERICA-11290', grupo_sanguineo='AB+'
            ),
            Paciente(
                id_pessoa=5, id_paciente=5, nome='Marlon Neto', cpf='837.851.729-77',
                data_nascimento=date(2016, 8, 26), is_flamengo=True, telefone='55(51)97295-3461',
                endereco='Campina Grande', num_convenio='UNIMED-77102', grupo_sanguineo='O-'
            ),
        ]
        session.add_all(pacientes)

        # 2. Preceptores 
        preceptores = [
            Preceptor(
                id_pessoa=6, id_profissional=6, id_preceptor=6, nome='Marcelo Iury', cpf='400.878.351-11',
                data_nascimento=date(2022, 9, 16), is_flamengo=True, telefone='55(71)95858-7524',
                endereco='Perto do Déde', crm='PB-12345', data_admissao=date(2015, 3, 1),
                especialidade='Ortopedia', titulacao='Chopper'
            ),
            Preceptor(
                id_pessoa=7, id_profissional=7, id_preceptor=7, nome='Neymar Jr', cpf='461.301.397-10',
                data_nascimento=date(1996, 4, 3), is_flamengo=False, telefone='55(41)95727-5013',
                endereco='Paris', crm='PB-22344', data_admissao=date(2016, 7, 10),
                especialidade='Oncologia', titulacao='Mestre'
            ),
            Preceptor(
                id_pessoa=8, id_profissional=8, id_preceptor=8, nome='Michael Scott', cpf='634.706.010-18',
                data_nascimento=date(1973, 1, 12), is_flamengo=True, telefone='55(85)96173-5506',
                endereco='Scranton', crm='PB-33456', data_admissao=date(2012, 1, 15),
                especialidade='Cirurgia Geral', titulacao='Doutor'
            ),
            Preceptor(
                id_pessoa=9, id_profissional=9, id_preceptor=9, nome='Clark Kent', cpf='826.526.064-04',
                data_nascimento=date(1943, 11, 2), is_flamengo=True, telefone='55(91)97894-7684',
                endereco='Gotham City', crm='PB-44567', data_admissao=date(2018, 9, 1),
                especialidade='Clínica Médica', titulacao='Especialista'
            ),
            Preceptor(
                id_pessoa=10, id_profissional=10, id_preceptor=10, nome='Bob Jackson', cpf='156.786.184-88',
                data_nascimento=date(1980, 12, 12), is_flamengo=False, telefone='55(41)94083-6938',
                endereco='Dalescott', crm='PB-55678', data_admissao=date(2010, 5, 20),
                especialidade='Emergência', titulacao='Doutor'
            ),
        ]
        session.add_all(preceptores)

        # 3. Residentes
        residentes = [
            Residente(
                id_pessoa=11, id_profissional=11, id_residente=11, nome='Alice Kennedy', cpf='130.776.889-76',
                data_nascimento=date(1929, 11, 9), is_flamengo=True, telefone='55(51)98561-9000',
                endereco='Scottsdale', crm='PB-66789', data_admissao=date(2023, 2, 1),
                especialidade='Ortopedia', ano_residencia=1
            ),
            Residente(
                id_pessoa=12, id_profissional=12, id_residente=12, nome='Drauzio Varella', cpf='085.784.728-33',
                data_nascimento=date(2011, 11, 9), is_flamengo=False, telefone='55(85)92621-7758',
                endereco='Rio de Janeiro', crm='PB-77890', data_admissao=date(2022, 8, 15),
                especialidade='Oncologia', ano_residencia=2
            ),
            Residente(
                id_pessoa=13, id_profissional=13, id_residente=13, nome='Oswaldo Cruz', cpf='491.691.164-83',
                data_nascimento=date(1929, 5, 3), is_flamengo=False, telefone='55(85)97973-7039',
                endereco='RJ', crm='PB-88901', data_admissao=date(2024, 1, 10),
                especialidade='Cirurgia Geral', ano_residencia=1
            ),
            Residente(
                id_pessoa=14, id_profissional=14, id_residente=14, nome='Antônio de Salles', cpf='981.246.846-10',
                data_nascimento=date(1992, 1, 14), is_flamengo=False, telefone='55(71)93021-1378',
                endereco='Casa Tão Engraçada', crm='PB-99012', data_admissao=date(2023, 6, 1),
                especialidade='Clínica Médica', ano_residencia=3
            ),
            Residente(
                id_pessoa=15, id_profissional=15, id_residente=15, nome='Angelita Habr-Gama', cpf='937.898.585-55',
                data_nascimento=date(2023, 11, 24), is_flamengo=False, telefone='55(71)93537-1108',
                endereco='Caixão', crm='PB-10123', data_admissao=date(2021, 3, 1),
                especialidade='Emergência', ano_residencia=2
            ),
        ]
        session.add_all(residentes)

        # 4. Unidades
        unidades = [
            Unidade(id_unidade=1, nome='Trauminha', tipo='Emergência Ortotraumatológica', capacidade_leitos=55),
            Unidade(id_unidade=2, nome='Oncologia', tipo='Tratamento de Câncer', capacidade_leitos=18),
            Unidade(id_unidade=3, nome='Centro Cirúrgico', tipo='Cirurgia', capacidade_leitos=40),
        ]
        session.add_all(unidades)

        # 5. Atendimentos
        atendimentos = [
            Atendimento(id_atendimento=10, id_paciente=1, id_residente=11, id_preceptor=6, data_hora=datetime(2026, 6, 1, 8, 30), duracao_minutos=Decimal('30.00')),
            Atendimento(id_atendimento=20, id_paciente=2, id_residente=12, id_preceptor=6, data_hora=datetime(2026, 6, 1, 9, 15), duracao_minutos=Decimal('45.00')),
            Atendimento(id_atendimento=30, id_paciente=3, id_residente=15, id_preceptor=7, data_hora=datetime(2026, 6, 2, 10, 0), duracao_minutos=Decimal('20.00')),
            Atendimento(id_atendimento=40, id_paciente=4, id_residente=11, id_preceptor=7, data_hora=datetime(2026, 6, 2, 11, 30), duracao_minutos=Decimal('60.00')),
            Atendimento(id_atendimento=50, id_paciente=5, id_residente=13, id_preceptor=8, data_hora=datetime(2026, 6, 3, 8, 0), duracao_minutos=Decimal('25.00')),
            Atendimento(id_atendimento=60, id_paciente=1, id_residente=14, id_preceptor=6, data_hora=datetime(2026, 6, 3, 14, 20), duracao_minutos=Decimal('40.00')),
            Atendimento(id_atendimento=70, id_paciente=2, id_residente=12, id_preceptor=8, data_hora=datetime(2026, 6, 4, 9, 45), duracao_minutos=Decimal('35.00')),
            Atendimento(id_atendimento=80, id_paciente=3, id_residente=11, id_preceptor=7, data_hora=datetime(2026, 6, 4, 13, 10), duracao_minutos=Decimal('15.00')),
            Atendimento(id_atendimento=90, id_paciente=4, id_residente=14, id_preceptor=8, data_hora=datetime(2026, 6, 5, 10, 30), duracao_minutos=Decimal('50.00')),
            Atendimento(id_atendimento=11, id_paciente=5, id_residente=15, id_preceptor=6, data_hora=datetime(2026, 6, 5, 16, 0), duracao_minutos=Decimal('30.00')),
        ]
        session.add_all(atendimentos)

        # 6. Níveis de Risco
        riscos = [
            NivelRisco(id_nivel_risco=1, nivel='BAIXO'),
            NivelRisco(id_nivel_risco=2, nivel='MEDIO'),
            NivelRisco(id_nivel_risco=3, nivel='ALTO'),
        ]
        session.add_all(riscos)

        # 7. Procedimentos
        procedimentos = [
            Procedimento(id_procedimento=1, codigo='PROC-0001', nome='Curativo Simples', tempo_medio_minutos=Decimal('20.00'), id_nivel_risco=1),
            Procedimento(id_procedimento=2, codigo='PROC-0002', nome='Sutura', tempo_medio_minutos=Decimal('35.00'), id_nivel_risco=2),
            Procedimento(id_procedimento=3, codigo='PROC-0003', nome='Drenagem', tempo_medio_minutos=Decimal('45.00'), id_nivel_risco=3),
            Procedimento(id_procedimento=4, codigo='PROC-0004', nome='Redução de Fratura', tempo_medio_minutos=Decimal('60.00'), id_nivel_risco=2),
            Procedimento(id_procedimento=5, codigo='PROC-0005', nome='Punção', tempo_medio_minutos=Decimal('15.00'), id_nivel_risco=2),
        ]
        session.add_all(procedimentos)

        # 8. Procedimentos Realizados
        procedimentos_realizados = [
            ProcedimentoRealizado(id_atendimento=10, id_procedimento=1, quantidade=1, tempo_real_minutos=Decimal('25.00'), observacao='Procedimento sem intercorrências', faturamento_processado=True),
            ProcedimentoRealizado(id_atendimento=20, id_procedimento=2, quantidade=2, tempo_real_minutos=Decimal('40.00'), observacao='Paciente colaborativo', faturamento_processado=False),
            ProcedimentoRealizado(id_atendimento=30, id_procedimento=1, quantidade=1, tempo_real_minutos=Decimal('18.00'), observacao=None, faturamento_processado=True),
            ProcedimentoRealizado(id_atendimento=40, id_procedimento=3, quantidade=1, tempo_real_minutos=Decimal('55.00'), observacao='Necessário auxílio do preceptor', faturamento_processado=False),
            ProcedimentoRealizado(id_atendimento=50, id_procedimento=2, quantidade=1, tempo_real_minutos=Decimal('20.00'), observacao='Realizado rapidamente', faturamento_processado=True),
            ProcedimentoRealizado(id_atendimento=60, id_procedimento=4, quantidade=3, tempo_real_minutos=Decimal('35.00'), observacao='Repetido devido a erro inicial', faturamento_processado=False),
            ProcedimentoRealizado(id_atendimento=70, id_procedimento=1, quantidade=1, tempo_real_minutos=Decimal('30.00'), observacao=None, faturamento_processado=False),
            ProcedimentoRealizado(id_atendimento=80, id_procedimento=5, quantidade=1, tempo_real_minutos=Decimal('12.00'), observacao='Procedimento simples', faturamento_processado=False),
            ProcedimentoRealizado(id_atendimento=90, id_procedimento=3, quantidade=2, tempo_real_minutos=Decimal('45.00'), observacao='Leve atraso no início', faturamento_processado=True),
            ProcedimentoRealizado(id_atendimento=11, id_procedimento=2, quantidade=1, tempo_real_minutos=Decimal('28.00'), observacao=None, faturamento_processado=True),
        ]
        session.add_all(procedimentos_realizados)

        # 9. Alergias
        alergias = [
            Alergia(id_alergia=10, id_pessoa=1, tipo_alergia='Ovo'),
            Alergia(id_alergia=20, id_pessoa=2, tipo_alergia='Poeira'),
            Alergia(id_alergia=30, id_pessoa=3, tipo_alergia='Dipirona'),
            Alergia(id_alergia=40, id_pessoa=4, tipo_alergia='Água'),
            Alergia(id_alergia=50, id_pessoa=5, tipo_alergia='Poeira'),
        ]
        session.add_all(alergias)

        session.commit()