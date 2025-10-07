from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.vereador_schema import VereadorCreate, VereadorPublic, PaginatedVereadorResponse, VereadorUpdate, VereadorSimple
from app.services.usuario_service import UsuarioService
from app.services.vereador_service import VereadorService
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.usuario_model import Usuario
from typing import List, Optional

router = APIRouter(prefix="/vereadores", tags=["Vereadores"])

@router.post("/", response_model=VereadorPublic, status_code=status.HTTP_201_CREATED)
def create_vereador(
    *,
    db: Session = Depends(get_db),
    vereador: VereadorCreate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Criar um novo vereador no sistema.
    """
    service = VereadorService(db)
    return service.create_vereador(vereador_create=vereador)


@router.get("/", response_model=PaginatedVereadorResponse)
def read_vereadores(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    filtro: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna uma lista de vereadores.
    """
    service = VereadorService(db)
    vereadores = service.get_all_vereadores(skip=skip, limit=limit, filtro=filtro)
    total = service.get_total_vereadores(filtro=filtro)
    return {"items": vereadores, "total": total}


@router.get("/{id}", response_model=VereadorPublic)
def read_vereador_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna um vereador específico pelo seu ID.
    """
    service = VereadorService(db)
    return service.get_vereador_by_id(id=id)


@router.get("/cpf/{cpf}", response_model=VereadorSimple)
def read_vereador_by_cpf(
    *,
    db: Session = Depends(get_db),
    cpf: str,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna um vereador específico pelo seu CPF.
    """
    service = VereadorService(db)
    return service.get_vereador_by_cpf(cpf=cpf)


@router.get("/email/{email}", response_model=VereadorSimple)
def read_vereador_by_email(
    *,
    db: Session = Depends(get_db),
    email: str,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Retorna um vereador específico pelo seu email.
    """
    service = VereadorService(db)
    return service.get_vereador_by_email(email=email)       


@router.put("/{id}", response_model=VereadorPublic)
def update_vereador(
    *,
    db: Session = Depends(get_db),
    id: int,
    vereador_update: VereadorUpdate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Atualiza um vereador existente.
    """
    service = VereadorService(db)
    return service.update_vereador(id=id, vereador_update=vereador_update)






