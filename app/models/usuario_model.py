# app/models/usuario_model.py
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship  # Importar relationship
from app.db.base import Base

class Usuario(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'usuario' no banco de dados.
    """
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    ativo = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    dt_cadastro = Column(TIMESTAMP, server_default=func.now())
    dt_atualizado = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

     # Relacionamento de volta para a tabela de associação
    # cascade="all, delete-orphan" garante que se um usuário for deletado,
    # suas associações também serão.
    associacoes = relationship("CamaraUsuario", back_populates="usuario", cascade="all, delete-orphan")