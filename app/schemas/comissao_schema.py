# app/schemas/comissao_schema.py
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Optional, List, Any
from datetime import datetime

# Propriedades base compartilhadas
class ComissaoBase(BaseModel):
    nome: str = Field(..., max_length=120)
    ativa: bool
    data_inicio: datetime
    data_fim: Optional[datetime] = None
    camara_id: int

# Schema para a criação de uma nova comissão
class ComissaoCreate(ComissaoBase):
    pass

# Schema para a atualização de uma comissão
class ComissaoUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=120)
    ativa: Optional[bool] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    camara_id: Optional[int] = None

# Schema principal para ser retornado pela API
class ComissaoPublic(ComissaoBase):
    id: int
    dt_cadastro: datetime

    # Correção 1: Redefinimos 'ativa' como 'int' para a saída da API.
    # Isto corrige o erro do Pydantic, pois o validador agora encontra
    # o campo 'ativa' definido diretamente nesta classe.
    ativa: int

    @field_validator('ativa', mode='before')
    @classmethod
    def bool_to_int(cls, v: Any) -> int:
        if isinstance(v, bool):
            return int(v)
        return v

    # Lógica para formatar as datas no padrão brasileiro
    @computed_field
    @property
    def data_inicio_formatada(self) -> str:
        """Formata a data de início para o padrão brasileiro."""
        return self.data_inicio.strftime('%d/%m/%Y')

    @computed_field
    @property
    def data_fim_formatada(self) -> Optional[str]:
        """Formata a data de fim para o padrão brasileiro."""
        # Correção 2: Adicionada verificação para evitar erro se data_fim for nula.
        # O código anterior tentaria formatar um valor 'None', causando um erro.
        if self.data_fim:
            return self.data_fim.strftime('%d/%m/%Y')
        return None
    
    @computed_field
    @property
    def dt_cadastro_formatada(self) -> str:
        """Formata a data de cadastro para o padrão brasileiro."""
        return self.dt_cadastro.strftime('%d/%m/%Y às %H:%M')
    
    class Config:
        from_attributes = True

# Schema para a resposta paginada
class PaginatedComissaoResponse(BaseModel):
    items: List[ComissaoPublic]
    total: int

