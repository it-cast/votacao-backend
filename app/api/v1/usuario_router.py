# app/api/v1/usuario_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UsuarioCreate, UsuarioPublic, PaginatedUsuarioResponse, UsuarioUpdate, UsuarioSimple
from app.services.usuario_service import UsuarioService
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.usuario_model import Usuario
from typing import List, Optional

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuarioPublic, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Cria um novo usuário no sistema.
    """
    service = UsuarioService(db)
    return service.create_usuario(usuario_create=usuario)

@router.get("/", response_model=PaginatedUsuarioResponse)
def read_usuarios(
    skip: int = 0,
    limit: int = 100,
    filtro: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Retorna uma lista de usuários.
    """
    service = UsuarioService(db)
    usuarios = service.get_all_usuarios(skip=skip, limit=limit, filtro=filtro)
    total = service.get_total_usuarios(filtro=filtro)
    return {"items": usuarios, "total": total}

@router.get("/me", response_model=UsuarioPublic)
def read_usuario_me(current_user: Usuario = Depends(get_current_user)):
    """
    Retorna os dados do usuário que está autenticado.
    """
    return current_user

@router.get("/{usuario_id}", response_model=UsuarioSimple)
def read_usuario_by_id(
    usuario_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Rota protegida
):
    """
    Retorna um usuário específico pelo ID.
    """
    service = UsuarioService(db)
    return service.get_usuario_by_id(usuario_id=usuario_id)


@router.get("/email/{email}", response_model=UsuarioSimple)
def read_usuario_by_email(
    email: str, 
    db: Session = Depends(get_db),
    current_User: Usuario = Depends(get_current_user) # Rota protegida
):
    """
    Retorna um usuário específico pelo email.
    """
    service = UsuarioService(db)
    return service.get_usuario_by_email(email=email)


@router.put("/{usuario_id}", response_model=UsuarioPublic)
def update_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Rota protegida
):
    """
    Atualiza um usuário.
    """
    service = UsuarioService(db)
    return service.update_usuario(usuario_id=usuario_id, usuario_update=usuario_update)

