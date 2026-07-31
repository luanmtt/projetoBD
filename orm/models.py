from datetime import date, datetime
from typing import Optional, List, Any, Dict
 
from sqlalchemy import (
    ForeignKey, String, Integer, Boolean, Date, DateTime, CheckConstraint,
    UniqueConstraint, Text, Numeric,
)

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


class Pessoa(Base):
    __tablename__ = "pessoa"

    id_pessoa:      Mapped[int] = mapped_column(primary_key = True)
    nome:           Mapped[str] = mapped_column(String(50), nullable = False)
    endereco:       Mapped[str] = mapped_column(String(50), nullable = False)
    is_flamengo:    Mapped[bool]= mapped_column(Boolean, default = False, nullable = False)

    cpf:            Mapped[str] = mapped_column(String(14), unique = True, nullable = False,
                                                default="000-000-000.00"
                                                )
    data_nascimento:Mapped[date]= mapped_column(Date, nullable = False,
                                                default="00/00/0000" 
                                                )
    telefone:       Mapped[str] = mapped_column(String(16), unique = True, nullable = False,
                                                default="00(00)00000-0000"
                                                )


    tipo_pessoa:    Mapped[str] = mapped_column(String(20))  # discriminador
 
    __mapper_args__ = {
        "polymorphic_identity": "pessoa",
        "polymorphic_on": "tipo_pessoa",
    }


class Paciente(Pessoa):
    __tablename__ = "paciente"
 
    id_paciente:    Mapped[int] = mapped_column(ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), primary_key=True)
    grupo_sanguineo:Mapped[str] = mapped_column(String(3), nullable=False)
    num_convenio:   Mapped[str] = mapped_column(String(20), unique=True, nullable=False,
                                                default="NOMECONVENIO-00000"
                                                )

    alergias:       Mapped[List["Alergia"]] = relationship(back_populates="pessoa")
    atendimentos:   Mapped[List["Atendimento"]] = relationship(back_populates="paciente")
    internacoes:    Mapped[List["Internacao"]] = relationship(back_populates="paciente")
 
    __mapper_args__ = {"polymorphic_identity": "paciente"}


class Profissional(Pessoa):
    __tablename__ = "profissional"
 
    id_profissional:Mapped[int] = mapped_column(ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), primary_key=True)
    especialidade:  Mapped[Optional[str]] = mapped_column(String(20), nullable=False)

    crm:            Mapped[str] = mapped_column(String(20), unique=True, nullable=False,
                                                default="AA-000000")
    data_admissao:  Mapped[date] = mapped_column(Date, nullable=False,
                                                 default="00/00/0000")
 

    papel_profissional: Mapped[str] = mapped_column(String(20))  # discriminador

    __mapper_args__ = {
        "polymorphic_identity": "profissional",
        "polymorphic_on": "papel_profissional",
    }


class Preceptor(Profissional):
    __tablename__ = "preceptor"
 
    id_preceptor:   Mapped[int] = mapped_column(ForeignKey("profissional.id_profissional", ondelete="CASCADE"), primary_key=True)
    titulacao:      Mapped[str] = mapped_column(String(20), nullable=False)
    escalas:        Mapped[List["Escala"]] = relationship(back_populates="preceptor")
 
    atendimentos_supervisionados: Mapped[List["Atendimento"]] = relationship(
        back_populates="preceptor"
    )

    __mapper_args__ = {"polymorphic_identity": "preceptor"}
 
 
class Residente(Profissional):
    __tablename__ = "residente"
 
    id_residente:   Mapped[int] = mapped_column(ForeignKey("profissional.id_profissional", ondelete="CASCADE"), primary_key=True)
    ano_residencia: Mapped[int] = mapped_column(Integer, nullable=False)

    atendimentos_realizados: Mapped[List["Atendimento"]] = relationship(back_populates="residente")
    escalas:        Mapped[List["Escala"]] = relationship(back_populates="residente")
 
    __mapper_args__ = {"polymorphic_identity": "residente"}
    

class Alergia(Base):
    __tablename__ = "alergia"

    id_alergia: Mapped[int] = mapped_column(primary_key=True)
    id_pessoa: Mapped[int] = mapped_column(ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), nullable=False)
    tipo_alergia: Mapped[str] = mapped_column(String(30), nullable=False)

    pessoa: Mapped["Pessoa"] = relationship(back_populates="alergias")

    __table_args__ = (
        UniqueConstraint("id_pessoa", "tipo_alergia", name="unq_pessoa"),
    )


class Unidade(Base):
    __tablename__ = "unidade"
    
    id_unidade: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(20), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    capacidade_leitos : Mapped[int] = mapped_column(Integer, 
                                                    CheckConstraint("capacidade_leitos >= 0"),
                                                    nullable=False)

class Atendimento(Base):
    __tablename__ = "atendimento"

    id_atendimento: Mapped[int] = mapped_column(primary_key = True)
    id_paciente:    Mapped[int] = mapped_column(ForeignKey("paciente.id_paciente", ondelete="CASCADE"), nullable=False)
    id_residente:   Mapped[int] = mapped_column(ForeignKey("residente.id_residente", ondelete="CASCADE"), nullable=False)
    id_preceptor:   Mapped[int] = mapped_column(ForeignKey("preceptor.id_preceptor", ondelete="CASCADE"), nullable=False)
    data_hora:      Mapped[date] = mapped_column(DateTime, nullable=False)
    duracao_minutos:Mapped[float] = mapped_column(Numeric(4,2), 
                                                  CheckConstraint("duracao_minutos >= 0"),
                                                  CheckConstraint("duracao_minutos < 1000"),
                                                  nullable=False,
                                                 )
    
    procedimentos_realizados: Mapped[List["ProcedimentoRealizado"]] = relationship(back_populates="atendimento")


class NivelRisco(Base):
    __tablename__ = "nivel_risco"

    id_nivel_risco: Mapped[int] = mapped_column(primary_key=True)
    nivel:  Mapped[str] = mapped_column(String(10), 
                                        CheckConstraint("nivel IN ('BAIXO', 'MEDIO', 'ALTO')"),
                                        unique=True, nullable=False)


class Procedimento(Base):
    __tablename__ = "procedimento"

    
    id_procedimento:Mapped[int] = mapped_column(primary_key=True)
    id_nivel_risco: Mapped[int] = mapped_column(ForeignKey("nivel_risco.id_nivel_risco", ondelete="CASCADE"), nullable=False)
    codigo:         Mapped[str] = mapped_column(String(9), nullable=False,
                                               default="PROC-0000"
                                               )
    nome:           Mapped[str] = mapped_column(String(50), nullable=False)
    tempo_medio_minutos: Mapped[float] = mapped_column(Numeric(4,2),nullable=False)

    realizacoes: Mapped[List["ProcedimentoRealizado"]] = relationship(back_populates="procedimento")

    __table_args__ = (
        CheckConstraint("tempo_medio_minutos >= 0"),
        CheckConstraint("tempo_medio_minutos < 1000"),
    )


class ProcedimentoRealizado(Base):
    __tablename__ = "procedimento_realizado"
    
    id_procedimento:Mapped[int] = mapped_column(ForeignKey("procedimento.id_procedimento",
                                                ondelete="CASCADE"),
                                                primary_key=True)

    id_atendimento:Mapped[int] = mapped_column(ForeignKey("atendimento.id_atendimento",
                                                ondelete="CASCADE"),
                                                primary_key=True)

    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    observacao: Mapped[str] = mapped_column(Text)

    data_hora_inicio: Mapped[date] = mapped_column(
            DateTime,
            nullable=False
        )
    
    tempo_real_minutos: Mapped[float] = mapped_column(Numeric(4,2), nullable=False)
    faturamento_processado:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    atendimento: Mapped["Atendimento"] = relationship(back_populates="procedimentos_realizados")
    procedimento: Mapped["Procedimento"] = relationship(back_populates="realizacoes")

    __table_args__ = (
        CheckConstraint("tempo_real_minutos >= 0"),
        CheckConstraint("tempo_real_minutos < 1000"),
    )
 

class Plantao(Base):
    __tablename__ = "plantao"

    id_plantao: Mapped[int] = mapped_column(primary_key=True)
    id_preceptor: Mapped[int] = mapped_column(ForeignKey("preceptor.id_preceptor", ondelete="CASCADE"), nullable=False)
    id_unidade: Mapped[int] = mapped_column(ForeignKey("unidade.id_unidade", ondelete="CASCADE"), nullable=False)
    dia_semana: Mapped[date] = mapped_column(Date, nullable=False)
    turno: Mapped[str] = mapped_column(String(10), nullable=False)

    __table_args__ = (
        CheckConstraint("turno IN ('manhã', 'tarde', 'noite')"),
        UniqueConstraint("id_unidade", "dia_semana", "turno", name="unq_plantao"),
    )

class Escala(Base):
    __tablename__ = "escala"

    id_escala: Mapped[int] = mapped_column(primary_key=True)
    id_plantao: Mapped[int] = mapped_column(ForeignKey("plantao.id_plantao", ondelete="CASCADE"), nullable=False)
    id_residente: Mapped[int] = mapped_column(ForeignKey("residente.id_residente", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("id_plantao", "id_residente", name="unq_escala"),
    )


class Internacao(Base):
    __tablename__ = "internacao"

    id_internacao: Mapped[int] = mapped_column(primary_key=True)
    id_paciente: Mapped[int] = mapped_column(ForeignKey("paciente.id_paciente", ondelete="CASCADE"), nullable=False)
    data_hora_entrada: Mapped[date] = mapped_column(DateTime, nullable=False)
    data_hora_saida: Mapped[date] = mapped_column(DateTime)

    paciente: Mapped["Paciente"] = relationship(back_populates="internacoes")

class Auditoria_atendimento(Base):
    __tablename__ = "auditoria_atendimento"

    id_auditoria: Mapped[int] = mapped_column(primary_key=True)
    id_atendimento: Mapped[int] = mapped_column(ForeignKey("atendimento.id_atendimento", ondelete="CASCADE"), nullable=False)
    data_hora: Mapped[date] = mapped_column(DateTime, nullable=False)
    operacao: Mapped[str] = mapped_column(String(10), 
                                          CheckConstraint("operacao IN (INSERT, UPDATE, DELETE)"),
                                          nullable=False)
    usuario: Mapped[str] = mapped_column(String(50), nullable=False)
    dados_novos: Mapped[Dict[str, Any]] = mapped_column(JSON)
    dados_antigos: Mapped[Dict[str, Any]] = mapped_column(JSON)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
