# app/schemas/vereador_schema.py
from operator import is_
from pydantic import BaseModel, EmailStr, Field, computed_field,field_validator, model_validator

from typing import Optional,List,Any
from datetime import datetime, date

class VereadorBase(BaseModel):
    email: EmailStr
    nome: str
    telefone: str
    cpf: str
    partido: str


# Schema para receber dados na criação de um usuário
class VereadorCreate(VereadorBase):
    id: Optional[int] = None
    ativo: bool = True



class VereadorUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    cpf: Optional[str] = None
    partido: Optional[str] = None
    ativo: Optional[bool] = None


# Usado para o retorno do get_by_id, com booleanos convertidos para 0 ou 1
class VereadorSimple(VereadorBase):
    id: int
    ativo: int

    @field_validator('ativo', mode='before')
    @classmethod
    def bool_to_int(cls, v: Any) -> int:
        if isinstance(v, bool):
            return int(v)
        return v

    class Config:
        from_attributes = True

# Schema para retornar dados públicos de um usuário (sem a senha)
class VereadorPublic(VereadorBase):
    id: int
    ativo: int 
    dt_cadastro: datetime
    dt_atualizado: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o Pydantic leia dados de objetos SQLAlchemy

# Schema principal para ser retornado pela API
class Vereador(VereadorPublic):

    @computed_field
    @property
    def ativo_desc(self) -> str:
        """ Retorna 'Sim' se o usuário estiver ativo, caso contrário 'Não'. """
        return "Sim" if self.ativo else "Não"

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

class PaginatedVereadorResponse(BaseModel):
    items: List[Vereador]
    total: int