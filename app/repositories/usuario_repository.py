# app/repositories/usuario_repository.py
from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate
from typing import List, Optional
from sqlalchemy import or_

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_by_id(self, id: int) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.id == id).first()
    
    
    def get_all(self, skip: int = 0, limit: int = 100, filtro: Optional[str] = None) -> list[Usuario]:
        query = self.db.query(Usuario)

        if filtro:
            query = query.filter(
                or_(
                    Usuario.email.ilike(f"%{filtro}%"),
                    Usuario.nome.ilike(f"%{filtro}%")
                )
            )

        return query.offset(skip).limit(limit).all()
    
    
    
    def create(self, usuario_create: UsuarioCreate, hashed_password: str) -> Usuario:
        db_usuario = Usuario(
            email   = usuario_create.email,
            nome    = usuario_create.nome,
            ativo   = usuario_create.ativo,
            is_superuser=usuario_create.is_superuser,
            senha_hash=hashed_password
        )
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario
    
    def update(self, db_obj: Usuario, obj_in: UsuarioUpdate, hashed_password: Optional[str] = None) -> Usuario:
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Se uma nova senha foi fornecida, atualiza o hash
        if hashed_password:
            update_data["senha_hash"] = hashed_password

        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    
    


    def count(self, filtro: Optional[str] = None) -> int:
        query = self.db.query(Usuario)
        if filtro:
            query = query.filter(
                or_(
                    Usuario.email.ilike(f"%{filtro}%"),
                    Usuario.nome.ilike(f"%{filtro}%")
                )
            )
        return query.count()