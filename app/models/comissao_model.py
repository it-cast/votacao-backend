from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Comissao(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'comissao' no banco de dados.
    """
    __tablename__ = "comissao"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(120), nullable=False)
    ativa = Column(Boolean, default=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=True)
    
    dt_cadastro = Column(TIMESTAMP, server_default=func.now())

    # Chave Estrangeira para a câmara
    camara_id = Column(Integer, ForeignKey("camara.id"), nullable=False)

    # Relacionamento de volta para a Câmara
    camara = relationship("Camara")