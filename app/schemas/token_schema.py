# app/schemas/token_schema.py
from pydantic import BaseModel
from app.schemas.usuario_schema import UsuarioPublic

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class TokenComUsuario(Token):
    usuario: UsuarioPublic