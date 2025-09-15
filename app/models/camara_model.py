from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Camara(Base):
    """
    Modelo SQLAlchemy que representa a tabela das camaras no banco de dados.
    """
    __tablename__ = "camara"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    cnpj = Column(String(20), unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    telefone = Column(String(20))
    endereco = Column(String(200))
    municipio = Column(String(120))
    uf = Column(String(2))
    numero_cadeiras = Column(Integer)
    
    dt_cadastro = Column(TIMESTAMP, server_default=func.now())
    dt_atualizado = Column(TIMESTAMP, onupdate=func.now())
    excluido = Column(Boolean, default=False)

    # Relacionamento de volta para a tabela de associação
    # Garante que o SQLAlchemy saiba que 'associacoes' em Camara se conecta com 'camara' em CamaraUsuario
    associacoes = relationship(
        "CamaraUsuario", 
        back_populates="camara", 
        cascade="all, delete-orphan"
    )