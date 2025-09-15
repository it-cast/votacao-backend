
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional


# Importações necessárias para o schema e serviço
from app.schemas.camara_schema import Camara, CamaraCreate, CamaraUpdate,PaginatedCamaraResponse
from app.services.camara_service import camara_service

# Importações para a dependência de banco de dados e autenticação
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.usuario_model import Usuario # Opcional, mas bom para clareza de tipo

# Define o prefixo e as tags do roteador
router = APIRouter(prefix="/camaras", tags=["Câmaras"])

# A variável "current_user" não será usada diretamente, mas a sua presença
# como dependência garante que a rota é protegida.
@router.post("/", response_model=Camara, status_code=status.HTTP_201_CREATED)
def create_camara(
    *,
    db: Session = Depends(get_db),
    camara_in: CamaraCreate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova camara. Requer autenticação.
    """
    return camara_service.create_camara(db, camara=camara_in)

@router.get("/", response_model=PaginatedCamaraResponse)
def read_camaras(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    filtro: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna uma lista de camaras. Requer autenticação.
    """
    camaras = camara_service.get_all_camaras(db, skip, limit, filtro)
    total = camara_service.get_total_camaras(db,filtro) # Você precisará criar este método
    return {"items": camaras, "total": total}

@router.get("/{camara_id}", response_model=Camara)
def read_camara(
    *,
    db: Session = Depends(get_db),
    camara_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna uma camara específica pelo ID. Requer autenticação.
    """
    return camara_service.get_camara(db, camara_id)

@router.put("/{camara_id}", response_model=Camara)
def update_camara(
    *,
    db: Session = Depends(get_db),
    camara_id: int,
    camara_in: CamaraUpdate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Atualiza uma camara. Requer autenticação.
    """
    return camara_service.update_camara(db, camara_id, camara_in)

@router.delete("/{camara_id}", response_model=Camara)
def delete_camara(
    *,
    db: Session = Depends(get_db),
    camara_id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Deleta (logicamente) uma camara. Requer autenticação.
    """
    return camara_service.delete_camara(db, camara_id)