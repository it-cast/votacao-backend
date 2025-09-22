# votacao-backend/app/schemas/comissao_membro_schema.py
from pydantic import BaseModel, computed_field
from typing import Optional, List
from datetime import date, datetime # 1. Importar 'date' e 'datetime'

from app.schemas.comissao_schema import ComissaoPublic
from app.schemas.mandato_vereador_schema import MandatoVereadorPublic


# Apenas os campos que podem ser atualizados, sem validação de senha
class ComissaoMembroInUpdate(BaseModel):
    id: int
    funcao: int
    data_inicio: date # Alterado para date para consistência
    data_fim: date    # Alterado para date para consistência

class ComissaoMembroBase(BaseModel):
    funcao: int
    data_inicio: date # Alterado para date
    data_fim: date    # Alterado para date
    comissao_id: int
    mandato_vereador_id: int
    # Adicionando dt_cadastro na base para que o Public possa acessá-lo
    dt_cadastro: datetime

class ComissaoMembroCreate(BaseModel):
    comissao_id: int
    mandato_vereador_id: int
    funcao: int
    data_inicio: date
    data_fim: date

# O schema para atualização deve ter todos os campos como opcionais
class ComissaoMembroUpdate(BaseModel):
    funcao: Optional[int] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None

class ComissaoMembroPublic(ComissaoMembroBase):
    id: int
    comissao: ComissaoPublic
    mandato_vereador: MandatoVereadorPublic

    @computed_field
    @property
    def data_inicio_formatada(self) -> str:
        """Formata a data de início para o padrão brasileiro."""
        return self.data_inicio.strftime('%d/%m/%Y')

    @computed_field
    @property
    def data_fim_formatada(self) -> str:
        """Formata a data de fim para o padrão brasileiro."""
        return self.data_fim.strftime('%d/%m/%Y')
    
    @computed_field
    @property
    def dt_cadastro_formatada(self) -> str:
        """Formata a data de cadastro para o padrão brasileiro."""
        return self.dt_cadastro.strftime('%d/%m/%Y às %H:%M')

    class Config:
        from_attributes = True

class PaginatedComissaoMembroResponse(BaseModel):
    items: List[ComissaoMembroPublic]
    total: int