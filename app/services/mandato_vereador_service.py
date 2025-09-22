# app/services/mandato_vereador_service.py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.mandato_vereador_repository import MandatoVereadorRepository
from app.repositories.vereador_repository import VereadorRepository
from app.repositories.mandato_repository import mandato_repository
from app.schemas.mandato_vereador_schema import (
    MandatoVereadorCreate, 
    MandatoVereadorBase, 
    MandatoVereadorUpdatePayload,
    MandatoVereadorUpdate
)
from app.schemas.vereador_schema import VereadorUpdate
from app.services.vereador_service import VereadorService

class MandatoVereadorService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = MandatoVereadorRepository(db)
        self.vereador_repo = VereadorRepository(db)
        self.mandato_repo = mandato_repository

    def get_association(self, id: int):
        association = self.repository.get_by_id(id=id)
        if not association:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação não encontrada")
        return association

    def get_associations_by_mandato(self, mandato_id: int, skip: int, limit: int, filtro: Optional[str] = None):
        mandato = self.mandato_repo.get(self.db, id=mandato_id)
        if not mandato:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mandato não encontrado")
        
        return self.repository.get_all_by_mandato_id(
            mandato_id=mandato_id, skip=skip, limit=limit, filtro=filtro
        )

    def get_total_associations_by_mandato(self, mandato_id: int, filtro: Optional[str] = None) -> int:
        return self.repository.count_by_mandato_id(mandato_id=mandato_id, filtro=filtro)
    
    def get_all_associations(self, camara_id: Optional[int] = None, mandato_ativo: Optional[bool] = None):
        """
        Busca e retorna associações com base em filtros genéricos.
        """
        return self.repository.get_all(self.db, camara_id=camara_id, mandato_ativo=mandato_ativo)

    def create_association(self, association_in: MandatoVereadorCreate):
        vereador_data = association_in.vereador
        vereador_id = vereador_data.id if vereador_data else association_in.vereador_id

        if vereador_id:
            vereador = self.vereador_repo.get_by_id(id=vereador_id)
            if not vereador:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vereador com ID {vereador_id} não encontrado.")
        elif vereador_data:
            vereador_service = VereadorService(self.db)
            try:
                new_vereador = vereador_service.create_vereador(vereador_create=vereador_data)
                vereador_id = new_vereador.id
            except HTTPException as e:
                raise e
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID do vereador ou dados para criação do vereador são necessários.")

        mandato = self.mandato_repo.get(self.db, id=association_in.mandato_id)
        if not mandato:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mandato não encontrado")
        
        
        existing_association = self.repository.get_by_vereador_and_mandato(
            vereador_id=vereador_id,
            mandato_id=association_in.mandato_id
        )
        if existing_association:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este vereador já está cadastrado neste mandato."
            )

        create_data = MandatoVereadorBase(
            vereador_id=vereador_id,
            mandato_id=association_in.mandato_id,
            funcao=association_in.funcao
        )
        
        return self.repository.create(obj_in=create_data)

    def update_association(self, id: int, association_in: MandatoVereadorUpdatePayload):
        db_association = self.get_association(id=id)

        # Atualiza dados do vereador
        vereador_data = association_in.vereador
        vereador_update_schema = VereadorUpdate(**vereador_data.model_dump())
        vereador_service = VereadorService(self.db)
        vereador_service.update_vereador(vereador_id=db_association.vereador_id, vereador_update=vereador_update_schema)
        
        # Prepara os campos da associação para o update
        update_data_schema = MandatoVereadorUpdate(funcao=association_in.funcao)
        
        return self.repository.update(db_obj=db_association, obj_in=update_data_schema)

    def delete_association(self, id: int):
        """Deleta uma associação pelo seu ID."""
        association = self.repository.get_by_id(id=id)
        if not association:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação não encontrada")
        
        self.repository.remove(id=id)
        return association