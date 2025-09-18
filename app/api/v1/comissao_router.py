from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.comissao_schema import ComissaoPublic, ComissaoCreate, ComissaoUpdate, PaginatedComissaoResponse
from app.services.comissao_service import ComissaoService
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/comissoes", tags=["Comissões"])

@router.post("/", response_model=ComissaoPublic, status_code=status.HTTP_201_CREATED)
def create_comissao(
    *,
    db: Session = Depends(get_db),
    comissao_in: ComissaoCreate,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoService(db)
    return service.create_comissao(comissao_in=comissao_in)

@router.get("/{id}", response_model=ComissaoPublic)
def read_comissao_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoService(db)
    return service.get_comissao(id=id)

@router.get("/camara/{camara_id}", response_model=PaginatedComissaoResponse)
def read_comissoes_by_camara(
    *,
    db: Session = Depends(get_db),
    camara_id: int,
    skip: int = 0,
    limit: int = 100,
    filtro: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoService(db)
    comissoes = service.get_all_comissoes_by_camara(camara_id=camara_id, skip=skip, limit=limit, filtro=filtro)
    total = service.get_total_comissoes_by_camara(camara_id=camara_id, filtro=filtro)
    return {"items": comissoes, "total": total}

@router.put("/{id}", response_model=ComissaoPublic)
def update_comissao(
    *,
    db: Session = Depends(get_db),
    id: int,
    comissao_in: ComissaoUpdate, 
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoService(db)
    return service.update_comissao(id=id, comissao_in=comissao_in)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comissao(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    service = ComissaoService(db)
    service.delete_comissao(id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
