# app/services/camera_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.camara_repository import camara_repository
from app.schemas.camara_schema import CamaraCreate, CamaraUpdate
from typing import Optional

class CamaraService:
    def create_camara(self, db: Session, camara: CamaraCreate):
        return camara_repository.create(db=db, obj_in=camara)

    def get_camara(self, db: Session, camara_id: int):
        db_camara = camara_repository.get(db, camara_id)
        if not db_camara:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camara não encontrada")
        return db_camara

    def get_all_camaras(self, db: Session, skip: int, limit: int,  filtro: Optional[str] = None):
        return camara_repository.get_multi(db, skip=skip, limit=limit, filtro=filtro)

    def update_camara(self, db: Session, camara_id: int, camara_update: CamaraUpdate):
        db_camara = self.get_camara(db, camara_id)
        return camara_repository.update(db=db, db_obj=db_camara, obj_in=camara_update)

    def delete_camara(self, db: Session, camara_id: int):
        db_camara = camara_repository.remove(db, camara_id=camara_id)
        if not db_camara:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camara não encontrada")
        return db_camara

    def get_total_camaras(self, db: Session,  filtro: Optional[str] = None):
        return camara_repository.count(db, filtro=filtro)
    
camara_service = CamaraService()
