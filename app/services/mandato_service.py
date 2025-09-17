# votacao-backend/app/services/mandato_service.py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.mandato_repository import mandato_repository
from app.repositories.camara_repository import camara_repository
from app.schemas.mandato_schema import MandatoCreate, MandatoUpdate

class MandatoService:
    def __init__(self, db: Session):
        """
        Construtor do serviço, que inicializa os repositórios necessários.
        """
        self.db = db
        self.repository = mandato_repository
        self.camara_repo = camara_repository

    def get_mandato(self, id: int):
        """
        Busca um mandato específico pelo ID.
        Lança uma exceção 404 se não for encontrado.
        """
        mandato = self.repository.get(self.db, id=id)
        if not mandato:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mandato não encontrado")
        return mandato

    def get_all_mandatos_by_camara(self, camara_id: int, skip: int, limit: int, filtro: Optional[str] = None):
        """
        Busca uma lista de mandatos para uma câmara específica, com paginação e filtro.
        """
        # Valida se a câmara existe antes de buscar os mandatos
        camara = self.camara_repo.get(self.db, camara_id=camara_id)
        if not camara:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Câmara não encontrada")
        
        return self.repository.get_all_by_camara_id(
            self.db, camara_id=camara_id, skip=skip, limit=limit, filtro=filtro
        )

    def get_total_mandatos_by_camara(self, camara_id: int, filtro: Optional[str] = None) -> int:
        """
        Retorna o número total de mandatos para uma câmara específica, aplicando o filtro.
        """
        return self.repository.count_by_camara_id(self.db, camara_id=camara_id, filtro=filtro)

    def create_mandato(self, mandato_in: MandatoCreate):
        """
        Cria um novo mandato.
        """
        # Valida se a câmara associada ao mandato existe
        camara = self.camara_repo.get(self.db, camara_id=mandato_in.camara_id)
        if not camara:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Câmara com ID {mandato_in.camara_id} não encontrada."
            )
        
        return self.repository.create(self.db, obj_in=mandato_in)

    def update_mandato(self, id: int, mandato_in: MandatoUpdate):
        """
        Atualiza um mandato existente.
        """
        # Primeiro, busca o mandato para garantir que ele existe
        db_mandato = self.get_mandato(id=id)
        
        return self.repository.update(self.db, db_obj=db_mandato, obj_in=mandato_in)
    
    def delete_mandato(self, id: int):
        """
        Remove um mandato.
        """
        # Verifica se o mandato existe antes de tentar remover
        mandato = self.get_mandato(id=id)
        
        deleted_mandato = self.repository.remove(self.db, id=mandato.id)
        
        return deleted_mandato is not None