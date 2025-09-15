# app/services/usuario_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash
from typing import Optional

class UsuarioService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def create_usuario(self, usuario_create: UsuarioCreate):
        if usuario_create.senha != usuario_create.confSenha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="As senhas não coincidem."
            )
        
        existing_user = self.repository.get_by_email(usuario_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um usuário com este e-mail já está cadastrado."
            )
        
        hashed_password = get_password_hash(usuario_create.senha)
        
        return self.repository.create(usuario_create, hashed_password)
    
    def get_usuario_by_id(self, usuario_id: int):
        usuario = self.repository.get_by_id(id=usuario_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return usuario
    
    
    def get_usuario_by_email(self, email: str):
        usuario = self.repository.get_by_email(email=email)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return usuario


    def update_usuario(self, usuario_id: int, usuario_update: UsuarioUpdate):
        db_usuario = self.get_usuario_by_id(usuario_id)

        # Verifica se o novo e-mail já está em uso por outro usuário
        if usuario_update.email and usuario_update.email != db_usuario.email:
            existing_user = self.repository.get_by_email(usuario_update.email)
            if existing_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="E-mail já cadastrado.")

        # Validação de senha
        if usuario_update.senha:
            if not usuario_update.confSenha:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmação de senha é obrigatória.")
            if usuario_update.senha != usuario_update.confSenha:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas não coincidem.")
            
            hashed_password = get_password_hash(usuario_update.senha)
            # Remove senhas do objeto de atualização para não salvar em texto plano
            del usuario_update.senha
            del usuario_update.confSenha
        else:
            hashed_password = None

        return self.repository.update(db_obj=db_usuario, obj_in=usuario_update, hashed_password=hashed_password)


    def get_all_usuarios(self, skip: int = 0, limit: int = 100, filtro: Optional[str] = None):
        return self.repository.get_all(skip=skip, limit=limit, filtro=filtro)
    
    def get_total_usuarios(self, filtro: Optional[str] = None):
        return self.repository.count(filtro=filtro)
  