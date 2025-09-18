# votacao-backend/app/models/mandato_model.py
from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Mandato(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'mandato' no banco de dados.
    """
    __tablename__ = "mandato"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descricao = Column(String(120), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    
    dt_cadastro = Column(TIMESTAMP, server_default=func.now())
    dt_atualizado = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Chave Estrangeira para a câmara
    camara_id = Column(Integer, ForeignKey("camara.id"), nullable=False)

    # Relacionamento de volta para a Câmara
    # Permite acessar o objeto 'camara' a partir de um objeto 'mandato'
    camara = relationship("Camara", back_populates="mandatos")

    associacoes = relationship("MandatoVereador", back_populates="mandato", cascade="all, delete-orphan")