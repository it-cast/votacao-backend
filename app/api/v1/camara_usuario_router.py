# app/api/v1/camara_usuario_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.camara_usuario_schema import CamaraUsuarioPublic, CamaraUsuarioCreate, CamaraUsuarioUpdate, CamaraUsuarioUpdatePayload, PaginatedCamaraUsuarioResponse
from app.services.camara_usuario_service import CamaraUsuarioService
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.usuario_model import Usuario

router = APIRouter(prefix="/usuario-camara", tags=["Usuários da câmara"])

@router.post("/", response_model=CamaraUsuarioPublic, status_code=status.HTTP_201_CREATED)
def create_association(
    *,
    db: Session = Depends(get_db),
    association_in: CamaraUsuarioCreate,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Cria uma nova associação entre um usuário e uma câmara.
    Requer autenticação.
    """
    service = CamaraUsuarioService(db)
    return service.create_association(association_in=association_in)

@router.get("/{id}", response_model=CamaraUsuarioPublic)
def read_association_by_id(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obtém os dados de uma associação específica pelo seu ID,
    incluindo os detalhes do usuário e da câmara.
    Requer autenticação.
    """
    service = CamaraUsuarioService(db)
    return service.get_association(id=id)

@router.get("/camara/{camara_id}", response_model=PaginatedCamaraUsuarioResponse)
def read_associations_by_camara(
    *,
    db: Session = Depends(get_db),
    camara_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Lista todos os usuários associados a uma câmara específica com paginação.
    Requer autenticação.
    """
    service = CamaraUsuarioService(db)
    usuarios = service.get_associations_by_camara(camara_id=camara_id, skip=skip, limit=limit)
    total = service.get_total_associations_by_camara(camara_id=camara_id)
    return {"items": usuarios, "total": total}

@router.put("/{id}", response_model=CamaraUsuarioPublic)
def update_association(
    *,
    db: Session = Depends(get_db),
    id: int,
    association_in: CamaraUsuarioUpdatePayload, 
    current_user: Usuario = Depends(get_current_user)
):
    service = CamaraUsuarioService(db)
    return service.update_association(id=id, association_in=association_in)

@router.delete("/{id}", response_model=CamaraUsuarioPublic)
def delete_association(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: Usuario = Depends(get_current_user)
):
    """
    Deleta (logicamente) uma associação.
    Requer autenticação.
    """
    service = CamaraUsuarioService(db)
    return service.delete_association(id=id)