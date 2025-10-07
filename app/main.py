from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base
from app.db.database import engine
from app.api.v1 import (
    auth_router, 
    camara_router, 
    usuario_router, 
    camara_usuario_router, 
    mandato_router, 
    vereador_router, 
    mandato_vereador_router,
    comissao_router,
    comissao_membro_router  
)

# Esta linha cria as tabelas no seu banco de dados se elas não existirem
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Votação",
    description="API para o sistema de votação.",
    version="1.0.0"
)

# Defina as origens permitidas (de onde seu front-end fará as requisições)
origins = [
    "http://localhost",
    "http://localhost:4200", # Endereço padrão do Angular em desenvolvimento
    "http://localhost:8080",
    "http://localhost:3000"
]

# Adicione o middleware de CORS à sua aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de origens que podem fazer requisições
    allow_credentials=True, # Permite cookies (importante para autenticação)
    allow_methods=["*"],    # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],    # Permite todos os cabeçalhos
)


# Inclui os roteadores da API
app.include_router(auth_router.router, prefix="/api/v1")
app.include_router(usuario_router.router, prefix="/api/v1")
app.include_router(camara_router.router, prefix="/api/v1")
app.include_router(camara_usuario_router.router, prefix="/api/v1")
app.include_router(mandato_router.router, prefix="/api/v1")
app.include_router(vereador_router.router, prefix="/api/v1")
app.include_router(mandato_vereador_router.router, prefix="/api/v1")
app.include_router(comissao_router.router, prefix="/api/v1")
app.include_router(comissao_membro_router.router, prefix="/api/v1")
