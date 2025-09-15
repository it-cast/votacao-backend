# app/services/camara_usuario_service.py
import json
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.camara_usuario_repository import camara_usuario_repository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.camara_repository import camara_repository
from app.schemas.camara_usuario_schema import CamaraUsuarioCreate, CamaraUsuarioUpdate, CamaraUsuarioBase, CamaraUsuarioUpdatePayload
from app.schemas.usuario_schema import UsuarioUpdate
from app.services.usuario_service import UsuarioService

class CamaraUsuarioService:
    def __init__(self, db: Session):
        """
        Construtor do serviço, que inicializa os repositórios necessários.
        """
        self.db = db
        self.repository = camara_usuario_repository
        self.usuario_repo = UsuarioRepository(db)
        self.camara_repo = camara_repository

    def get_association(self, id: int):
        association = self.repository.get(self.db, id=id)
        if not association:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação não encontrada")
        return association

    def get_associations_by_camara(self, camara_id: int, skip: int, limit: int):
        cam = self.camara_repo.get(self.db, camara_id=camara_id)
        if not cam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câmara não encontrada")
        
        return self.repository.get_all_by_camara_id(
            self.db, camara_id=camara_id, skip=skip, limit=limit
        )

    def get_total_associations_by_camara(self, camara_id: int) -> int:
        """Retorna o número total de associações para uma câmara específica."""
        return self.repository.count_by_camara_id(self.db, camara_id=camara_id)

    def create_association(self, association_in: CamaraUsuarioCreate):
        if not association_in.usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O objeto 'usuario' é obrigatório para criar ou associar."
            )

        usuario_data = association_in.usuario
        usuario_id = usuario_data.id

        # --- PONTO DE DEBUG 1: VER O QUE CHEGA DO FRONTEND ---
        print("\n--- DEBUG: DADOS RECEBIDOS PELO SERVIÇO ---")
        print(f"Tipo de association_in.permissao: {type(association_in.permissao)}")
        print(f"Valor de association_in.permissao: {association_in.permissao}")
        print("-------------------------------------------\n")
        if usuario_id:
            user = self.usuario_repo.get_by_id(id=usuario_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuário com ID {usuario_id} não encontrado.")
        else:
            usuario_service = UsuarioService(self.db)
            try:
                new_user = usuario_service.create_usuario(usuario_create=usuario_data)
                usuario_id = new_user.id
            except HTTPException as e:
                raise e
        
        cam = self.camara_repo.get(self.db, camara_id=association_in.camara_id)
        if not cam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câmara não encontrada")

        existing_association = self.repository.get_by_usuario_and_camara(
            self.db, usuario_id=usuario_id, camara_id=association_in.camara_id
        )

        permissao_str = json.dumps(association_in.permissao)

        if existing_association:
            if existing_association.excluido:
                update_data = CamaraUsuarioUpdate(papel=association_in.papel, ativo=True)
                existing_association.excluido = False
                setattr(existing_association, 'permissao', permissao_str)
                return self.repository.update(self.db, db_obj=existing_association, obj_in=update_data)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Este usuário já está associado a esta câmara."
                )

        create_data_dict = {
            "usuario_id": usuario_id,
            "camara_id": association_in.camara_id,
            "papel": association_in.papel,
            "permissao": permissao_str
        }
        
        final_obj_to_create = CamaraUsuarioBase(**create_data_dict)

        # --- PONTO DE DEBUG 2: VER O OBJETO FINAL ANTES DE ENVIAR PARA O REPOSITÓRIO ---
        print("\n--- DEBUG: DADOS A SEREM ENVIADOS PARA O REPOSITÓRIO ---")
        print(f"Tipo de final_obj_to_create.permissao: {type(final_obj_to_create.permissao)}")
        print(f"Valor de final_obj_to_create.permissao: {final_obj_to_create.permissao}")
        print("------------------------------------------------------\n")
        return self.repository.create(self.db, obj_in=final_obj_to_create)

    def update_association(self, id: int, association_in: CamaraUsuarioUpdatePayload):
        db_association = self.get_association(id=id)

        # Atualiza dados do usuário (sem senha)
        usuario_data = association_in.usuario
        usuario_update_schema = UsuarioUpdate(
            nome=usuario_data.nome,
            email=usuario_data.email,
            ativo=usuario_data.ativo,
            is_superuser=usuario_data.is_superuser
        )
        usuario_service = UsuarioService(self.db)
        usuario_service.update_usuario(usuario_id=db_association.usuario_id, usuario_update=usuario_update_schema)

        # Atualiza permissões
        permissao_str = json.dumps(association_in.permissao)
        setattr(db_association, 'permissao', permissao_str)

        # Prepara os outros campos da associação para o update
        update_data_schema = CamaraUsuarioUpdate(
            papel=association_in.papel,
            ativo=association_in.ativo
        )
        
        return self.repository.update(self.db, db_obj=db_association, obj_in=update_data_schema)
    
    def delete_association(self, id: int):
        deleted_association = self.repository.remove(self.db, id=id)
        if not deleted_association:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associação não encontrada")
        return deleted_association