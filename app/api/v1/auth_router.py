# app/api/v1/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
# ATUALIZADO: Importe o novo schema
from app.schemas.token_schema import TokenComUsuario
from app.core.security import create_access_token, verify_password
from app.repositories.usuario_repository import UsuarioRepository

router = APIRouter(tags=["Autenticação"])

# ATUALIZADO: Altere o response_model para o novo schema
@router.post("/login", response_model=TokenComUsuario)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user_repo = UsuarioRepository(db)
    usuario = user_repo.get_by_email(form_data.username) 
    
    if not usuario or not verify_password(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": usuario.email})
    
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "usuario": usuario 
    }