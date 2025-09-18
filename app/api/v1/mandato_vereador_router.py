# app/api/v1/mandato_vereador_router.py
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.mandato_vereador_schema import (
    MandatoVereadorPublic, 
    MandatoVereadorCreate, 
    PaginatedMandatoVereadorResponse,
    MandatoVereadorUpdatePayload
)
from app.services.mandato_vereador_service import MandatoVereadorService
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/mandato-vereador", tags=["Associação Mandato/Vereador"])

@router.post("/", response_model=MandatoVereadorPublic, status_code=status.HTTP_201_CREATED)
def create_association(
    *,
    db: Session = Depends(get_db),
    association_in: MandatoVereadorCreate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova associação entre um vereador e um mandato.
    Pode-se passar um 'vereador_id' para associar um existente,
    ou um objeto 'vereador' completo para criar um novo e associá-lo.
    """
    service = MandatoVereadorService(db)
    return service.create_association(association_in=association_in)

@router.get("/mandato/{mandato_id}", response_model=PaginatedMandatoVereadorResponse)
def read_associations_by_mandato(
    *,
    db: Session = Depends(get_db),
    mandato_id: int,
    skip: int = 0,
    limit: int = 100,
    filtro: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Lista todos os vereadores associados a um mandato específico, com paginação e filtro.
    """
    service = MandatoVereadorService(db)
    associacoes = service.get_associations_by_mandato(mandato_id=mandato_id, skip=skip, limit=limit, filtro=filtro)
    total = service.get_total_associations_by_mandato(mandato_id=mandato_id, filtro=filtro)
    return {"items": associacoes, "total": total}

@router.get("/{id}", response_model=MandatoVereadorPublic)
def read_association_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Busca os dados de uma associação específica pelo seu ID.
    """
    service = MandatoVereadorService(db)
    return service.get_association(id=id)

@router.put("/{id}", response_model=MandatoVereadorPublic)
def update_association(
    *,
    db: Session = Depends(get_db),
    id: int,
    association_in: MandatoVereadorUpdatePayload,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Atualiza os dados de uma associação (função) e os dados do vereador associado.
    """
    service = MandatoVereadorService(db)
    return service.update_association(id=id, association_in=association_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_association(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Deleta uma associação entre um vereador e um mandato.
    """
    service = MandatoVereadorService(db)
    service.delete_association(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)