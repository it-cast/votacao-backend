from tokenize import String
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class MandatoVereador(Base):
    """
    Modelo da tabela associativa entre Mandato e Vereador,
    definindo o papel de cada Vereador em um mandato.
    """
    __tablename__ = "mandato_vereador"

    id = Column(Integer, primary_key=True, index=True)
    funcao = Column(Integer, nullable=False, comment="Define a função do vereador no mandato.")

    # Chaves Estrangeiras
    mandato_id = Column(Integer, ForeignKey("mandato.id"), nullable=False)
    vereador_id = Column(Integer, ForeignKey("vereador.id"), nullable=False)

    # Relacionamentos (permite acessar os objetos completos)
    mandato = relationship("Mandato", back_populates="associacoes")
    vereador = relationship("Vereador", back_populates="associacoes")

    associacoes = relationship("ComissaoMembro", back_populates="mandato_vereador", cascade="all, delete-orphan")
    