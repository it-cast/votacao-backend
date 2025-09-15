# app/repositories/camara_repository.py
from sqlalchemy.orm import Session
from app.models.camara_model import Camara
from app.schemas.camara_schema import CamaraCreate, CamaraUpdate
from typing import List, Optional
from sqlalchemy import or_

class CamaraRepository:
    def get(self, db: Session, camara_id: int) -> Optional[Camara]:
        """
        Busca uma única câmara pelo ID.
        """
        return db.query(Camara).filter(Camara.id == camara_id, Camara.excluido == False).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, filtro: Optional[str] = None) -> List[Camara]:
        """
        Busca uma lista de câmaras com paginação.
        """
        query = db.query(Camara).filter(Camara.excluido == False)

        if filtro:
            query = query.filter(
                or_(
                    Camara.nome.ilike(f"%{filtro}%"),
                    Camara.municipio.ilike(f"%{filtro}%"),
                    Camara.uf.ilike(f"%{filtro}%"),
                )
            )


        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CamaraCreate) -> Camara:
        """
        Cria uma nova câmara no banco de dados.
        """
        # Atualizado para Pydantic V2
        db_obj = Camara(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Camara, obj_in: CamaraUpdate
    ) -> Camara:
        """
        Atualiza os dados de uma câmara existente.
        """
        # Atualizado para Pydantic V2
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, camara_id: int) -> Optional[Camara]:
        """
        Realiza a exclusão lógica (soft delete) de uma câmara.
        """
        db_obj = self.get(db, camara_id)
        if not db_obj:
            return None
        
        db_obj.excluido = True
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def count(self, db: Session, filtro: Optional[str] = None) -> int:
        """
        Conta o número total de câmaras não excluídas, aplicando o filtro se houver.
        """
        query = db.query(Camara).filter(Camara.excluido == False)

        if filtro:
            query = query.filter(
                or_(
                    Camara.nome.ilike(f"%{filtro}%"),
                    Camara.municipio.ilike(f"%{filtro}%"),
                    Camara.uf.ilike(f"%{filtro}%")
                )
            )
        return query.count()

camara_repository = CamaraRepository()

