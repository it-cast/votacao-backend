# app/repositories/mandato_vereador_repository.py
from sqlalchemy.orm import Session
from app.models.vereador_model import Vereador
from app.models.mandato_model import Mandato
from app.models.mandato_vereador_model import MandatoVereador
from app.schemas.mandato_vereador_schema import MandatoVereadorBase, MandatoVereadorUpdate
from typing import List, Optional
from sqlalchemy import or_

class MandatoVereadorRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[MandatoVereador]:
        """Busca uma associação pelo seu ID."""
        return self.db.query(MandatoVereador).filter(MandatoVereador.id == id).first()
    
    def get_by_vereador_and_mandato(self, *, vereador_id: int, mandato_id: int) -> Optional[MandatoVereador]:
        """Busca uma associação específica pelo ID do vereador e do mandato."""
        return self.db.query(MandatoVereador).filter(
            MandatoVereador.vereador_id == vereador_id,
            MandatoVereador.mandato_id == mandato_id
        ).first()
    
    def get_all_by_mandato_id(self, mandato_id: int, skip: int = 0, limit: int = 100, filtro: Optional[str] = None) -> List[MandatoVereador]:
        """Busca todas as associações de um mandato, com filtro e paginação."""
        query = self.db.query(MandatoVereador).filter(MandatoVereador.mandato_id == mandato_id)

        if filtro:
            query = query.join(Vereador, MandatoVereador.vereador_id == Vereador.id)
            query = query.filter(
                or_(
                    Vereador.nome.ilike(f"%{filtro}%"),
                    Vereador.email.ilike(f"%{filtro}%")
                )
            )

        return query.offset(skip).limit(limit).all()
    
    
    def get_all(
        self, 
        db: Session, 
        *,
        camara_id: Optional[int] = None,
        mandato_ativo: Optional[bool] = None
    ) -> List[MandatoVereador]:
        """
        Busca genérica de associações com filtros opcionais.
        """
        query = db.query(MandatoVereador)
        
        # Se filtros relacionados ao mandato forem fornecidos, faz o JOIN
        if camara_id is not None or mandato_ativo is not None:
            query = query.join(Mandato) # Junta MandatoVereador com Mandato
            
            if camara_id is not None:
                query = query.filter(Mandato.camara_id == camara_id)
            
            if mandato_ativo is not None:
                query = query.filter(Mandato.ativo == mandato_ativo)

        return query.all()
    

    def create(self, obj_in: MandatoVereadorBase) -> MandatoVereador:
        """Cria uma nova associação no banco de dados."""
        db_obj = MandatoVereador(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: MandatoVereador, obj_in: MandatoVereadorUpdate) -> MandatoVereador:
        """Atualiza uma associação existente."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def remove(self, id: int) -> Optional[MandatoVereador]:
        """Remove uma associação do banco de dados pelo ID."""
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
        return db_obj
        
    def count_by_mandato_id(self, mandato_id: int, filtro: Optional[str] = None) -> int:
        """Conta o total de associações para um mandato, com filtro."""
        query = self.db.query(MandatoVereador).filter(MandatoVereador.mandato_id == mandato_id)
        
        if filtro:
            query = query.join(Vereador, MandatoVereador.vereador_id == Vereador.id)
            query = query.filter(
                or_(
                    Vereador.nome.ilike(f"%{filtro}%"),
                    Vereador.email.ilike(f"%{filtro}%")
                )
            )
        return query.count()