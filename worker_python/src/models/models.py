import enum

from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.sql import func

from src.core.database import Base


class TipoRemetente(str, enum.Enum):
    cliente = "cliente"
    bot = "bot"
    advogado = "advogado"


class StatusAtendimento(str, enum.Enum):
    triagem = "triagem"
    encaminhado = "encaminhado"
    finalizado = "finalizado"


class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(150), nullable=True)
    telefone = Column(String(20), unique=True, index=True, nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now())


class AdvogadoModel(Base):
    __tablename__ = "advogados"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    especialidade = Column(String(100), nullable=False)
    whatsapp = Column(String(20), nullable=False)
    disponivel = Column(Boolean, default=True)
    criado_em = Column(TIMESTAMP, server_default=func.now())


class AtendimentoModel(Base):
    __tablename__ = "atendimentos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    advogado_id = Column(Integer, ForeignKey("advogados.id"), nullable=True)
    categoria_inferida = Column(String(100), nullable=True)
    status = Column(
        SQLAlchemyEnum(StatusAtendimento), default=StatusAtendimento.triagem
    )
    resumo_ia = Column(Text, nullable=True)
    criado_em = Column(TIMESTAMP, server_default=func.now())


class MensagemModel(Base):
    __tablename__ = "mensagens"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    atendimento_id = Column(Integer, ForeignKey("atendimentos.id", ondelete="CASCADE"))
    remetente = Column(SQLAlchemyEnum(TipoRemetente), nullable=False)
    conteudo = Column(Text, nullable=False)
    criado_em = Column(TIMESTAMP, server_default=func.now())
