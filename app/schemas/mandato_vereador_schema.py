from pydantic import BaseModel
from typing import Optional, List

from app.schemas.vereador_schema import VereadorCreate, VereadorPublic
from app.schemas.mandato_schema import MandatoPublic

# Apenas os campos que podem ser atualizados, sem validação de senha
class VereadorInUpdate(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool


class MandatoVereadorUpdatePayload(BaseModel):
    mandato_id: int
    funcao: int
    vereador: VereadorInUpdate

class MandatoVereadorBase(BaseModel):
    vereador_id: int
    mandato_id: int
    funcao: int

class MandatoVereadorCreate(BaseModel):
    mandato_id: int
    funcao: int
    vereador: Optional[VereadorCreate] = None
    vereador_id: Optional[int] = None

# O schema para atualização deve ter todos os campos como opcionais,
# pois ele é usado para atualizações parciais.
class MandatoVereadorUpdate(BaseModel):
    funcao: Optional[int] = None

class MandatoVereadorPublic(MandatoVereadorBase):
    id: int
    funcao: int
    vereador: VereadorPublic
    mandato: MandatoPublic
    class Config:
        from_attributes = True

class PaginatedMandatoVereadorResponse(BaseModel):
    items: List[MandatoVereadorPublic]
    total: int

