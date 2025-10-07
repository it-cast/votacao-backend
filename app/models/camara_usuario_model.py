# app/models/camara_usuario_model.py
from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, Text, func, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class CamaraUsuario(Base):
    """
    Modelo da tabela associativa entre Câmara e Usuário,
    definindo o papel de cada usuário em uma câmara.
    """
    __tablename__ = "camara_usuario"

    id = Column(Integer, primary_key=True, index=True)
    
    # O papel do usuário (ex: 1 para 'Admin', 2 para 'Visualizador', etc.)
    papel = Column(Integer, nullable=False, comment="Define o nível de permissão do usuário na câmara.")

    permissao = Column(Text, nullable=False, comment="Define as permissões específicas do usuário em formato de texto (ex: JSON).")
    
    ativo = Column(Boolean, default=True)
    excluido = Column(Boolean, default=False)

    
    dt_cadastro = Column(TIMESTAMP, server_default=func.now())
    dt_atualizado = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Chaves Estrangeiras
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    camara_id = Column(Integer, ForeignKey("camara.id"), nullable=False)
    vereador_id = Column(Integer, ForeignKey("vereador.id"), nullable=True)

    # Relacionamentos (permite acessar os objetos completos)
    usuario = relationship("Usuario", back_populates="associacoes")
    camara = relationship("Camara", back_populates="associacoes")
    vereador = relationship("Vereador", back_populates="camaraUsuarios")