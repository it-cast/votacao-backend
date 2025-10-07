from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.vereador_repository import VereadorRepository

from app.schemas.vereador_schema import VereadorCreate, VereadorUpdate
from typing import Optional

class VereadorService:
    def __init__(self, db: Session):
        self.repository = VereadorRepository(db)
    
    def get_all_vereadores(self, skip: int = 0, limit: int = 100, filtro: Optional[str] = None):
        return self.repository.get_all(skip=skip, limit=limit, filtro=filtro)
    
    def get_total_vereadores(self, filtro: Optional[str] = None):
        return self.repository.count(filtro=filtro)
    
    def create_vereador(self, vereador_create: VereadorCreate):
        existing_vereador = self.repository.get_by_email(vereador_create.email)
        existing_vereador_cpf = self.repository.get_by_cpf(vereador_create.cpf)

        if existing_vereador or existing_vereador_cpf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um vereador com este e-mail ou CPF já está cadastrado."
            )
        
        return self.repository.create(vereador_create)
    
    def update_vereador(self, id: int, vereador_update: VereadorUpdate):
        db_vereador = self.get_vereador_by_id(id)
        if not db_vereador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vereador não encontrado"
            )
        
        return self.repository.update(db_obj=db_vereador, obj_in=vereador_update)
    
    def get_vereador_by_id(self, id: int):
        vereador = self.repository.get_by_id(id=id)
        if not vereador:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vereador não encontrado")
        return vereador
    
    def get_vereador_by_email(self, email: str):
        vereador = self.repository.get_by_email(email=email)
        if not vereador:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vereador não encontrado"
            )
        return vereador
    
    def get_vereador_by_cpf(self, cpf: str):
        vereador = self.repository.get_by_cpf(cpf=cpf)
        if not vereador:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Vereador não encontrado"
            )
        return vereador
    
    
    
        