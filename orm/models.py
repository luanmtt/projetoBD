from datetime import date, datetime
from typing import Optional, List
 
from sqlalchemy import (
    ForeignKey, String, Integer, Boolean, Date, DateTime, CheckConstraint,
    UniqueConstraint, Text, Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
 
from database import Base

class Pessoa(Base):
    __tablename__ = "pessoa"

    id_pessoa = Mapped[int] = mapped_column(primary_key = True)
    nome: Mapped[str] = mapped_column(String(50), nullable = False)
    cpf: Mapped[str] = mapped_column(String(14), unique = True, nullable = False)
    nome: Mapped[date] = mapped_column(Date, nullable = False)
    is_flamengo: Mapped[bool] = mapped_column(Boolean, default = False, nullable = False)
    telefone: Mapped[str] = mapped_column(String(16), unique = True, nullable = False)

    tipo_pessoa: Mapped[str] = mapped_column(String(20))  # discriminador
 
    __mapper_args__ = {
        "polymorphic_identity": "pessoa",
        "polymorphic_on": "tipo_pessoa",
    }

class Paciente(Pessoa):
    __tablename__ = "paciente"
 
    id_pessoa: Mapped[int] = mapped_column(ForeignKey("pessoa.id_pessoa"), primary_key=True)
    num_convenio: Mapped[str] = mapped_column(String(30))
    alergias: Mapped[str] = mapped_column(Text)
    grupo_sanguineo: Mapped[str] = mapped_column(String(3))
 
    atendimentos: Mapped[List["Atendimento"]] = relationship(back_populates="paciente")
    internacoes: Mapped[List["Internacao"]] = relationship(back_populates="paciente")
 
    __mapper_args__ = {"polymorphic_identity": "paciente"}

class Profissional(Pessoa):
    __tablename__ = "profissional"
 
    id_pessoa: Mapped[int] = mapped_column(ForeignKey("pessoa.id_pessoa"), primary_key=True)
    crm: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    data_admissao: Mapped[date] = mapped_column(Date, nullable=False)
    especialidade: Mapped[Optional[str]] = mapped_column(String(80))
 
    papel_profissional: Mapped[str] = mapped_column(String(20))  # discriminador
 
    __mapper_args__ = {
        "polymorphic_identity": "profissional",
        "polymorphic_on": "papel_profissional",
    }

class Preceptor(Profissional):
    __tablename__ = "preceptor"
 
    id_profissional: Mapped[int] = mapped_column(ForeignKey("profissional.id_pessoa"), primary_key=True)
    titulacao: Mapped[str] = mapped_column(String(30), nullable=False)
 
    atendimentos_supervisionados: Mapped[List["Atendimento"]] = relationship(
        back_populates="preceptor"
    )
    escalas: Mapped[List["Escala"]] = relationship(back_populates="preceptor")
 
    __mapper_args__ = {"polymorphic_identity": "preceptor"}
 
 
class Residente(Profissional):
    __tablename__ = "residente"
 
    id_profissional: Mapped[int] = mapped_column(ForeignKey("profissional.id_pessoa"), primary_key=True)
    ano_residencia: Mapped[int] = mapped_column(Integer, nullable=False)
 
    atendimentos_realizados: Mapped[List["Atendimento"]] = relationship(back_populates="residente")
    escalas: Mapped[List["Escala"]] = relationship(back_populates="residente")
 
    __mapper_args__ = {"polymorphic_identity": "residente"}