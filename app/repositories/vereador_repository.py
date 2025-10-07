from sqlalchemy.orm import Session
from app.models.vereador_model import Vereador
from app.schemas.vereador_schema import VereadorCreate, VereadorUpdate, PaginatedVereadorResponse
from typing import List, Optional
from sqlalchemy import or_

class VereadorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100, filtro: Optional[str] = None) -> PaginatedVereadorResponse:
        query = self.db.query(Vereador)
        if filtro:
            query = query.filter(
                or_(
                    Vereador.nome.ilike(f"%{filtro}%"),
                    Vereador.email.ilike(f"%{filtro}%")
                )
            )
        return query.offset(skip).limit(limit).all()
    
    def count(self, filtro: Optional[str] = None) -> int:
        query = self.db.query(Vereador)
        if filtro:
            query = query.filter(
                or_(
                    Vereador.nome.ilike(f"%{filtro}%"),
                    Vereador.email.ilike(f"%{filtro}%")
                )
            )
        return query.count()

    def get_by_email(self, email: str) -> Vereador | None:
        return self.db.query(Vereador).filter(Vereador.email == email).first()
    
    def get_by_id(self, id: int) -> Vereador | None:
        return self.db.query(Vereador).filter(Vereador.id == id).first()
    
    def get_by_cpf(self, cpf: str) -> Vereador | None:
        return self.db.query(Vereador).filter(Vereador.cpf == cpf).first()
    
    def create(self, vereador_create: VereadorCreate) -> Vereador:
        vereador_create = Vereador(**vereador_create.model_dump())
        self.db.add(vereador_create)
        self.db.commit()
        self.db.refresh(vereador_create)

        return vereador_create
    
    def update(self, db_obj: Vereador, obj_in: VereadorUpdate) -> Vereador:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
        