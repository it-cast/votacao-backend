# app/repositories/comissao_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.comissao_model import Comissao
from app.schemas.comissao_schema import ComissaoCreate, ComissaoUpdate
from typing import List, Optional

class ComissaoRepository:
    def get(self, db: Session, id: int) -> Optional[Comissao]:
        return db.query(Comissao).filter(Comissao.id == id).first()

    def get_all_by_camara_id(self, db: Session, *, camara_id: int, skip: int = 0, limit: int = 100, filtro: Optional[str] = None) -> List[Comissao]:
        query = db.query(Comissao).filter(Comissao.camara_id == camara_id)
        if filtro:
            query = query.filter(Comissao.nome.ilike(f"%{filtro}%"))
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: ComissaoCreate) -> Comissao:
        db_obj = Comissao(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Comissao, obj_in: ComissaoUpdate) -> Comissao:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[Comissao]:
        db_obj = self.get(db, id=id)
        if not db_obj:
            return None
        db.delete(db_obj)
        db.commit()
        return db_obj

    def count_by_camara_id(self, db: Session, *, camara_id: int, filtro: Optional[str] = None) -> int:
        query = db.query(Comissao).filter(Comissao.camara_id == camara_id)
        if filtro:
            query = query.filter(Comissao.nome.ilike(f"%{filtro}%"))
        return query.count()

comissao_repository = ComissaoRepository()
