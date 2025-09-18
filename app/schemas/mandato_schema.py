from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Optional, List, Any
from datetime import date, datetime

# Importa o schema da Câmara para o relacionamento
from app.schemas.camara_schema import CamaraSimple

# Propriedades base compartilhadas
class MandatoBase(BaseModel):
    descricao: str = Field(..., max_length=120)
    ativo: bool 
    data_inicio: date
    data_fim: date
    camara_id: int

# Schema para a criação de um novo mandato
class MandatoCreate(MandatoBase):
    pass # Todos os campos da base são obrigatórios na criação

# Schema para a atualização de um mandato (todos os campos são opcionais)
class MandatoUpdate(BaseModel):
    descricao: Optional[str] = Field(None, max_length=120)
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    ativo: Optional[bool] = None
    # camara_id geralmente não é alterado, mas pode ser incluído se necessário
    # camara_id: Optional[int] = None

# Schema principal para ser retornado pela API
class MandatoPublic(MandatoBase):
    id: int
    dt_cadastro: datetime
    dt_atualizado: Optional[datetime] = None

    ativo: int

    @field_validator('ativo', mode='before')
    @classmethod
    def bool_to_int(cls, v: Any) -> int:
        if isinstance(v, bool):
            return int(v)
        return v
    
    # Aninha os dados da câmara relacionada para um retorno mais completo
    camara: CamaraSimple

    # Lógica para formatar as datas no padrão brasileiro
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
        from_attributes = True # Permite que o Pydantic leia dados de objetos SQLAlchemy

# Schema para a resposta paginada
class PaginatedMandatoResponse(BaseModel):
    items: List[MandatoPublic]
    total: int
    
class MensagemResposta(BaseModel):
    detalhe: str
