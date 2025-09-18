# votacao-backend/app/repositories/mandato_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from app.models.mandato_model import Mandato
from app.schemas.mandato_schema import MandatoCreate, MandatoUpdate

class MandatoRepository:
    def get(self, db: Session, id: int) -> Optional[Mandato]:
        """
        Busca um único mandato pelo ID.
        """
        return db.query(Mandato).filter(Mandato.id == id).first()

    def get_all_by_camara_id(self, db: Session, *, camara_id: int, skip: int = 0, limit: int = 100, filtro: Optional[str] = None) -> List[Mandato]:
        """
        Busca uma lista de mandatos de uma câmara, com paginação e filtro.
        """
        query = db.query(Mandato).filter(Mandato.camara_id == camara_id)

        if filtro:
            # Filtra pela descrição do mandato
            query = query.filter(Mandato.descricao.ilike(f"%{filtro}%"))

        return query.offset(skip).limit(limit).all()

    def count_by_camara_id(self, db: Session, *, camara_id: int, filtro: Optional[str] = None) -> int:
        """
        Conta o número total de mandatos para uma câmara específica,
        aplicando o filtro se fornecido.
        """
        query = db.query(Mandato).filter(Mandato.camara_id == camara_id)

        if filtro:
            query = query.filter(Mandato.descricao.ilike(f"%{filtro}%"))
            
        return query.count()

    def create(self, db: Session, *, obj_in: MandatoCreate) -> Mandato:
        """
        Cria um novo mandato na base de dados.
        """
        db_obj_data = obj_in.model_dump()
        db_obj = Mandato(**db_obj_data)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Mandato, obj_in: MandatoUpdate) -> Mandato:
        """
        Atualiza um mandato existente.
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[Mandato]:
        """
        Remove um mandato da base de dados (deleção física).
        """
        db_obj = self.get(db, id=id)
        if not db_obj:
            return None
        
        db.delete(db_obj)
        db.commit()
        return db_obj

    def deactivate_all_active_by_camara(self, db: Session, *, camara_id: int, exclude_id: Optional[int] = None):
        """
        Desativa todos os mandatos ativos de uma câmara, opcionalmente excluindo um ID.
        """
        query = db.query(Mandato).filter(Mandato.camara_id == camara_id, Mandato.ativo == True)
        
        if exclude_id:
            query = query.filter(Mandato.id != exclude_id)
            
        mandatos_to_deactivate = query.all()
        
        for mandato in mandatos_to_deactivate:
            mandato.ativo = False
            db.add(mandato)
        
        db.commit()


# Instância única do repositório para ser usada em toda a aplicação
mandato_repository = MandatoRepository()
