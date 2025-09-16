# app/schemas/token_schema.py
from pydantic import BaseModel
from typing import Optional, List
from app.schemas.usuario_schema import UsuarioPublic
from app.schemas.camara_schema import CamaraSimple

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class TokenComUsuario(Token):
    usuario: UsuarioPublic
    camaras: Optional[List[CamaraSimple]] = None