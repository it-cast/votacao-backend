# votacao-backend/app/services/comissao_membro_service.py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.comissao_membro_repository import ComissaoMembroRepository
from app.repositories.comissao_repository import comissao_repository
from app.repositories.mandato_vereador_repository import MandatoVereadorRepository
from app.schemas.comissao_membro_schema import ComissaoMembroCreate, ComissaoMembroUpdate

class ComissaoMembroService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ComissaoMembroRepository(db)
        self.comissao_repo = comissao_repository
        self.mandato_vereador_repo = MandatoVereadorRepository(db)

    def get_association(self, id: int):
        association = self.repository.get_by_id(id=id)
        if not association:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação não encontrada")
        return association

    def get_all_by_comissao_id(self, comissao_id: int, skip: int, limit: int, filtro: Optional[str] = None):
        comissao = self.comissao_repo.get(self.db, id=comissao_id)
        if not comissao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comissão não encontrada")
        
        return self.repository.get_all_by_comissao_id(
            comissao_id=comissao_id, skip=skip, limit=limit, filtro=filtro
        )

    def get_total_by_comissao_id(self, comissao_id: int, filtro: Optional[str] = None) -> int:
        return self.repository.count_by_comissao_id(comissao_id=comissao_id, filtro=filtro)

    def create_association(self, association_in: ComissaoMembroCreate):
        # Valida se a comissão existe
        comissao = self.comissao_repo.get(self.db, id=association_in.comissao_id)
        if not comissao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comissão não encontrada")
        
        # Valida se o mandato_vereador (associação) existe
        mandato_vereador = self.mandato_vereador_repo.get_by_id(id=association_in.mandato_vereador_id)
        if not mandato_vereador:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vereador do mandato não encontrado")
            
        return self.repository.create(obj_in=association_in)

    def update_association(self, id: int, association_in: ComissaoMembroUpdate):
        db_association = self.get_association(id=id)
        return self.repository.update(db_obj=db_association, obj_in=association_in)
    
    def delete_association(self, id: int):
        association = self.get_association(id=id)
        self.repository.remove(id=association.id)
        return {"detail": "Membro da comissão deletado com sucesso."}