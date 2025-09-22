# votacao-backend/app/repositories/comissao_membro_repository.py
from sqlalchemy.orm import Session
from app.models.comissao_membro import ComissaoMembro
from app.models.mandato_vereador_model import MandatoVereador
from app.models.vereador_model import Vereador
from app.schemas.comissao_membro_schema import ComissaoMembroCreate, ComissaoMembroUpdate
from typing import List, Optional
from sqlalchemy import or_

class ComissaoMembroRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[ComissaoMembro]:
        return self.db.query(ComissaoMembro).filter(ComissaoMembro.id == id).first()

    def get_all_by_comissao_id(self, comissao_id: int, skip: int = 0, limit: int = 100, filtro: Optional[str] = None) -> List[ComissaoMembro]:
        query = self.db.query(ComissaoMembro).filter(ComissaoMembro.comissao_id == comissao_id)

        if filtro:
            query = query.join(MandatoVereador).join(Vereador).filter(
                or_(
                    Vereador.nome.ilike(f"%{filtro}%"),
                    Vereador.partido.ilike(f"%{filtro}%")
                )
            )

        return query.offset(skip).limit(limit).all()

    def count_by_comissao_id(self, comissao_id: int, filtro: Optional[str] = None) -> int:
        query = self.db.query(ComissaoMembro).filter(ComissaoMembro.comissao_id == comissao_id)

        if filtro:
            query = query.join(MandatoVereador).join(Vereador).filter(
                or_(
                    Vereador.nome.ilike(f"%{filtro}%"),
                    Vereador.partido.ilike(f"%{filtro}%")
                )
            )
        
        return query.count()

    def create(self, obj_in: ComissaoMembroCreate) -> ComissaoMembro:
        db_obj = ComissaoMembro(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ComissaoMembro, obj_in: ComissaoMembroUpdate) -> ComissaoMembro:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, id: int) -> Optional[ComissaoMembro]:
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
        return db_obj