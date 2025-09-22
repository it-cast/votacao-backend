# votacao-backend/app/api/v1/comissao_membro_router.py
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.comissao_membro_schema import (
    ComissaoMembroPublic, 
    ComissaoMembroCreate, 
    ComissaoMembroUpdate,
    PaginatedComissaoMembroResponse
)
from app.services.comissao_membro_service import ComissaoMembroService
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/comissao-membros", tags=["Membros da Comissão"])

@router.post("/", response_model=ComissaoMembroPublic, status_code=status.HTTP_201_CREATED)
def create_comissao_membro(
    *,
    db: Session = Depends(get_db),
    comissao_membro_in: ComissaoMembroCreate,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoMembroService(db)
    return service.create_association(association_in=comissao_membro_in)

@router.get("/comissao/{comissao_id}", response_model=PaginatedComissaoMembroResponse)
def read_comissao_membros(
    *,
    db: Session = Depends(get_db),
    comissao_id: int,
    skip: int = 0,
    limit: int = 100,
    filtro: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoMembroService(db)
    membros = service.get_all_by_comissao_id(comissao_id=comissao_id, skip=skip, limit=limit, filtro=filtro)
    total = service.get_total_by_comissao_id(comissao_id=comissao_id, filtro=filtro)
    return {"items": membros, "total": total}

@router.get("/{id}", response_model=ComissaoMembroPublic)
def read_comissao_membro_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoMembroService(db)
    return service.get_association(id=id)

@router.put("/{id}", response_model=ComissaoMembroPublic)
def update_comissao_membro(
    *,
    db: Session = Depends(get_db),
    id: int,
    comissao_membro_in: ComissaoMembroUpdate,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoMembroService(db)
    return service.update_association(id=id, association_in=comissao_membro_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comissao_membro(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoMembroService(db)
    service.delete_association(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)