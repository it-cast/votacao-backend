# app/schemas/camara_usuario_schema.py
from pydantic import BaseModel
from typing import Optional, List

from app.schemas.usuario_schema import UsuarioPublic, UsuarioSimple, UsuarioCreate
from app.schemas.camara_schema import Camara
from app.schemas.vereador_schema import Vereador

# Apenas os campos que podem ser atualizados, sem validação de senha
class UsuarioInUpdate(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool
    is_superuser: bool


class CamaraUsuarioUpdatePayload(BaseModel):
    ativo: bool
    camara_id: int
    papel: int
    vereador_id: Optional[int] = None
    permissao: List[str]
    usuario: UsuarioInUpdate

class CamaraUsuarioBase(BaseModel):
    usuario_id: int
    camara_id: int
    vereador_id: Optional[int] = None
    papel: int
    permissao: str

class CamaraUsuarioCreate(BaseModel):
    camara_id: int
    papel: int
    permissao: List[str]
    ativo: Optional[bool] = True
    usuario: Optional[UsuarioCreate] = None
    usuario_id: Optional[int] = None
    vereador_id: Optional[int] = None


# O schema para atualização deve ter todos os campos como opcionais,
# pois ele é usado para atualizações parciais.
class CamaraUsuarioUpdate(BaseModel):
    papel: Optional[int] = None
    ativo: Optional[bool] = None
    vereador_id: Optional[int] = None


class CamaraUsuarioPublic(CamaraUsuarioBase):
    id: int
    ativo: bool
    usuario: UsuarioSimple
    camara: Camara
    vereador: Optional[Vereador] = None
    class Config:
        from_attributes = True

class PaginatedCamaraUsuarioResponse(BaseModel):
    items: List[CamaraUsuarioPublic]
    total: int