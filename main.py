from fastapi import FastAPI
from routers.documentos import router as documentos_router
from routers import consultas
from routers.infra import router as infra_router
from core.logger import logger

app = FastAPI(
    title="Cofre Digital - Manutenção de Equipamentos",
    description="API para gestão de documentos e metadados de manutenção de equipamentos.",
    version="1.0.0"
)

# Registar os roteadores
app.include_router(documentos_router)
app.include_router(consultas.router)
app.include_router(infra_router)

@app.on_event("startup")
async def startup_event():
    logger.info("SISTEMA_INICIADO Cofre Digital carregado com sucesso.")

@app.get("/", tags=["Root"])
def root():
    return {"mensagem": "API do Cofre Digital está a funcionar com sucesso!"}