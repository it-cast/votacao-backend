# app/schemas/usuario_schema.py
from operator import is_
from pydantic import BaseModel, EmailStr, Field, computed_field,field_validator, model_validator

from typing import Optional,List,Any
from datetime import datetime

class UsuarioBase(BaseModel):
    email: EmailStr
    nome: str
    


# Schema para receber dados na criação de um usuário
class UsuarioCreate(UsuarioBase):
    id: Optional[int] = None
    senha: Optional[str] = Field(None, min_length=4)
    confSenha: Optional[str] = Field(None, min_length=4)
    ativo: bool = True
    is_superuser: bool = False

    # --- CORREÇÃO APLICADA AQUI ---
    @model_validator(mode='before')
    @classmethod
    def check_passwords(cls, data: Any):
        """
        Valida senhas para utilizadores novos e limpa-as para utilizadores existentes.
        """
        if isinstance(data, dict):
            user_id = data.get('id')
            senha = data.get('senha')

            if user_id:
                # SE O UTILIZADOR JÁ EXISTE:
                # Se a senha for uma string vazia ou None, removemos para evitar a validação de min_length.
                if not senha: # Pega tanto "" quanto None
                    data.pop('senha', None)
                    data.pop('confSenha', None)
            else:
                # SE O UTILIZADOR É NOVO:
                # A senha e a confirmação são obrigatórias.
                conf_senha = data.get('confSenha')
                if not senha or not conf_senha:
                    raise ValueError('Senha e confirmação de senha são obrigatórias para novos utilizadores')
                if senha != conf_senha:
                    raise ValueError('As senhas não coincidem')
        
        return data


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    confSenha: Optional[str] = None
    ativo: Optional[bool] = None
    is_superuser: Optional[bool] = None

# Usado para o retorno do get_by_id, com booleanos convertidos para 0 ou 1
class UsuarioSimple(UsuarioBase):
    id: int
    ativo: int
    is_superuser: int

    @field_validator('ativo', 'is_superuser', mode='before')
    @classmethod
    def bool_to_int(cls, v: Any) -> int:
        if isinstance(v, bool):
            return int(v)
        return v

    class Config:
        from_attributes = True

# Schema para retornar dados públicos de um usuário (sem a senha)
class UsuarioPublic(UsuarioBase):
    id: int
    ativo: bool
    is_superuser: bool
    dt_cadastro: datetime
    dt_atualizado: Optional[datetime] = None

    class Config:
        from_attributes = True # Permite que o Pydantic leia dados de objetos SQLAlchemy

# Schema principal para ser retornado pela API
class Usuario(UsuarioPublic):
    
    # --- LÓGICA DE FORMATAÇÃO COM CAMPOS COMPUTADOS ---
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

class PaginatedUsuarioResponse(BaseModel):
    items: List[Usuario]
    total: int