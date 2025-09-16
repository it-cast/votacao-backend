from pydantic import BaseModel, EmailStr, Field, computed_field
from typing import Optional,List
from datetime import datetime

# Propriedades compartilhadas que todos os schemas terão
class CamaraBase(BaseModel):
    nome: Optional[str] = Field(None, max_length=120)
    cnpj: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[str] = Field(None, max_length=200)
    municipio: Optional[str] = Field(None, max_length=120)
    uf: Optional[str] = Field(None, max_length=2)
    numero_cadeiras: Optional[int] = None

# Schema para a criação de uma nova câmera (campos obrigatórios)
class CamaraCreate(CamaraBase):
    nome: str = Field(..., max_length=120)
    email: EmailStr

# Schema para a atualização de uma câmera (todos os campos são opcionais)
class CamaraUpdate(CamaraBase):
    pass

# Schema para representar os dados vindos do banco de dados
class CamaraInDB(CamaraBase):
    id: int
    dt_cadastro: datetime
    dt_atualizado: Optional[datetime] = None
    excluido: bool

    class Config:
        from_attributes = True

# Schema principal para ser retornado pela API
class Camara(CamaraInDB):
    @computed_field
    @property
    def dt_cadastro_formatada(self) -> str:
        """ Formata a data de cadastro para o padrão brasileiro. """
        # Acessa diretamente o atributo 'dt_cadastro' que já foi validado.
        return self.dt_cadastro.strftime('%d/%m/%Y às %H:%M')

    @computed_field
    @property
    def dt_atualizado_formatada(self) -> Optional[str]:
        """ Formata a data de atualização para o padrão brasileiro. """
        # Acessa diretamente o atributo 'dt_atualizado'.
        if self.dt_atualizado:
            return self.dt_atualizado.strftime('%d/%m/%Y às %H:%M')
        return None

class PaginatedCamaraResponse(BaseModel):
    items: List[Camara]
    total: int

class CamaraSimple(BaseModel):
    """Schema simplificado para retornar dados básicos da Câmara."""
    id: int
    nome: str

    class Config:
        from_attributes = True