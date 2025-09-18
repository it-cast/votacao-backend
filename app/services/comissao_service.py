# app/services/comissao_service.py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.comissao_repository import comissao_repository
from app.repositories.camara_repository import camara_repository
from app.schemas.comissao_schema import ComissaoCreate, ComissaoUpdate

class ComissaoService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = comissao_repository
        self.camara_repo = camara_repository

    def get_comissao(self, id: int):
        comissao = self.repository.get(self.db, id=id)
        if not comissao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comissão não encontrada")
        return comissao

    def get_all_comissoes_by_camara(self, camara_id: int, skip: int, limit: int, filtro: Optional[str] = None):
        camara = self.camara_repo.get(self.db, camara_id=camara_id)
        if not camara:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câmara não encontrada")
        
        return self.repository.get_all_by_camara_id(
            self.db, camara_id=camara_id, skip=skip, limit=limit, filtro=filtro
        )

    def get_total_comissoes_by_camara(self, camara_id: int, filtro: Optional[str] = None) -> int:
        return self.repository.count_by_camara_id(self.db, camara_id=camara_id, filtro=filtro)

    def create_comissao(self, comissao_in: ComissaoCreate):
        camara = self.camara_repo.get(self.db, camara_id=comissao_in.camara_id)
        if not camara:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Câmara com ID {comissao_in.camara_id} não encontrada."
            )
        
        return self.repository.create(self.db, obj_in=comissao_in)

    def update_comissao(self, id: int, comissao_in: ComissaoUpdate):
        db_comissao = self.get_comissao(id=id)
        return self.repository.update(self.db, db_obj=db_comissao, obj_in=comissao_in)
    
    def delete_comissao(self, id: int):
        comissao = self.get_comissao(id=id)
        self.repository.remove(self.db, id=comissao.id)
        return {"detail": "Comissão deletada com sucesso."}
