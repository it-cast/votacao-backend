# votacao-backend/app/api/v1/mandato_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

# 1. Importações dos schemas de Mandato
from app.schemas.mandato_schema import MandatoPublic, MandatoCreate, MandatoUpdate, PaginatedMandatoResponse, MensagemResposta


# 2. Importação do serviço de Mandato
from app.services.mandato_service import MandatoService

# 3. Importações padrão para dependências
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.usuario_model import Usuario

# 4. Definição do router
router = APIRouter(prefix="/mandatos", tags=["Mandatos"])

@router.post("/", response_model=MandatoPublic, status_code=status.HTTP_201_CREATED)
def create_mandato(
    *,
    db: Session = Depends(get_db),
    mandato_in: MandatoCreate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria um novo mandato. Requer autenticação.
    """
    service = MandatoService(db)
    return service.create_mandato(mandato_in=mandato_in)

@router.get("/{id}", response_model=MandatoPublic)
def read_mandato_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtém os dados de um mandato específico pelo seu ID.
    Requer autenticação.
    """
    service = MandatoService(db)
    return service.get_mandato(id=id)

@router.get("/camara/{camara_id}", response_model=PaginatedMandatoResponse)
def read_mandatos_by_camara(
    *,
    db: Session = Depends(get_db),
    camara_id: int,
    skip: int = 0,
    limit: int = 100,
    filtro: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Lista todos os mandatos associados a uma câmara específica com paginação.
    Requer autenticação.
    """
    service = MandatoService(db)
    mandatos = service.get_all_mandatos_by_camara(camara_id=camara_id, skip=skip, limit=limit, filtro=filtro)
    total = service.get_total_mandatos_by_camara(camara_id=camara_id, filtro=filtro)
    return {"items": mandatos, "total": total}

@router.put("/{id}", response_model=MandatoPublic)
def update_mandato(
    *,
    db: Session = Depends(get_db),
    id: int,
    mandato_in: MandatoUpdate, 
    current_user: Usuario = Depends(get_current_user)
):
    """
    Atualiza um mandato existente. Requer autenticação.
    """
    service = MandatoService(db)
    return service.update_mandato(id=id, mandato_in=mandato_in)

@router.delete("/{id}", response_model=MensagemResposta)
def delete_mandato(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Deleta um mandato. Requer autenticação.
    """
    service = MandatoService(db)
    service.delete_mandato(id=id) 

    # Retorna uma mensagem de sucesso que corresponde ao schema MensagemResposta
    return {"detalhe": "Mandato deletado com sucesso."}