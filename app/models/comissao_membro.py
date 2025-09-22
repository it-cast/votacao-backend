from tokenize import String
from sqlalchemy import Column, Integer, ForeignKey, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class ComissaoMembro(Base):
    """
    Modelo da tabela associativa entre comissão e mandato_vereador,
    definindo o papel de cada Vereador em uma comissão.
    """
    __tablename__ = "comissao_membro"

    id = Column(Integer, primary_key=True, index=True)
    funcao = Column(Integer, nullable=False, comment="Define a função do vereador na comissao.")

    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)

    dt_cadastro = Column(TIMESTAMP, server_default=func.now())

    # Chaves Estrangeiras
    comissao_id = Column(Integer, ForeignKey("comissao.id"), nullable=False)
    mandato_vereador_id = Column(Integer, ForeignKey("mandato_vereador.id"), nullable=False)

    # Relacionamentos (permite acessar os objetos completos)
    comissao = relationship("Comissao", back_populates="associacoes")
    mandato_vereador = relationship("MandatoVereador", back_populates="associacoes")
    