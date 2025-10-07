# app/models/usuario_model.py
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship  # Importar relationship
from app.db.base import Base

class Vereador(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'vereador' no banco de dados.
    """
    __tablename__ = "vereador"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=False)
    telefone = Column(String(20), nullable=False)
    partido = Column(String(45), nullable=False)

   
    ativo = Column(Boolean, default=True)
   
    
    dt_cadastro = Column(TIMESTAMP, server_default=func.now())
    dt_atualizado = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    associacoes = relationship("MandatoVereador", back_populates="vereador", cascade="all, delete-orphan")
    camaraUsuarios = relationship("CamaraUsuario", back_populates="vereador", cascade="all, delete-orphan")