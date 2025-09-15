# app/repositories/camara_usuario_repository.py
from sqlalchemy.orm import Session
from app.models.camara_usuario_model import CamaraUsuario
# ATUALIZADO: Importe CamaraUsuarioBase em vez de CamaraUsuarioCreate
from app.models.usuario_model import Usuario
from app.schemas.camara_usuario_schema import CamaraUsuarioBase, CamaraUsuarioUpdate
from typing import List, Optional
from sqlalchemy import or_

class CamaraUsuarioRepository:
    def get(self, db: Session, id: int) -> Optional[CamaraUsuario]:
        return db.query(CamaraUsuario).filter(CamaraUsuario.id == id, CamaraUsuario.excluido == False).first()

    def get_by_usuario_and_camara(self, db: Session, *, usuario_id: int, camara_id: int) -> Optional[CamaraUsuario]:
        return db.query(CamaraUsuario).filter(
            CamaraUsuario.usuario_id == usuario_id,
            CamaraUsuario.camara_id == camara_id
        ).first()

    def get_all_by_camara_id(self, db: Session, *, camara_id: int, skip: int = 0, limit: int = 100, filtro: Optional[str] = None) -> List[CamaraUsuario]:
        """
        Busca uma lista de associações de uma câmara, com JOIN para permitir
        filtrar pelo nome ou e-mail do usuário.
        """
        query = db.query(CamaraUsuario).filter(
            CamaraUsuario.camara_id == camara_id, 
            CamaraUsuario.excluido == False
        )

        if filtro:
            # Adiciona o JOIN com a tabela Usuario
            query = query.join(Usuario, CamaraUsuario.usuario_id == Usuario.id)
            # Adiciona o filtro para nome ou e-mail
            query = query.filter(
                or_(
                    Usuario.nome.ilike(f"%{filtro}%"),
                    Usuario.email.ilike(f"%{filtro}%")
                )
            )

        return query.offset(skip).limit(limit).all()

    # --- 3. FUNÇÃO DE CONTAGEM ATUALIZADA ---
    def count_by_camara_id(self, db: Session, *, camara_id: int, filtro: Optional[str] = None) -> int:
        """
        Conta o número total de associações para uma câmara específica,
        aplicando o filtro de nome ou e-mail se fornecido.
        """
        query = db.query(CamaraUsuario).filter(
            CamaraUsuario.camara_id == camara_id, 
            CamaraUsuario.excluido == False
        )

        if filtro:
            # Adiciona o JOIN com a tabela Usuario
            query = query.join(Usuario, CamaraUsuario.usuario_id == Usuario.id)
            # Adiciona o filtro para nome ou e-mail
            query = query.filter(
                or_(
                    Usuario.nome.ilike(f"%{filtro}%"),
                    Usuario.email.ilike(f"%{filtro}%")
                )
            )
            
        return query.count()

    # --- CORREÇÃO APLICADA AQUI ---
    # A função agora espera `CamaraUsuarioBase`, que tem `permissao` como uma string.
    def create(self, db: Session, *, obj_in: CamaraUsuarioBase) -> CamaraUsuario:
        """
        Cria uma nova associação na base de dados.
        """
        # Usamos model_dump() para criar um dicionário a partir do schema Pydantic,
        # garantindo a compatibilidade com o construtor do SQLAlchemy.
        db_obj_data = obj_in.model_dump()
        db_obj = CamaraUsuario(**db_obj_data)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: CamaraUsuario, obj_in: CamaraUsuarioUpdate) -> CamaraUsuario:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[CamaraUsuario]:
        db_obj = self.get(db, id=id)
        if not db_obj:
            return None
        
        db_obj.excluido = True
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

   

camara_usuario_repository = CamaraUsuarioRepository()