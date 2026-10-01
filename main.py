from fastapi import FastAPI
from routers.documentos import router as documentos_router
from routers import consultas

app = FastAPI(
    title="Cofre Digital - Manutenção de Equipamentos",
    description="API para gestão de documentos e metadados de manutenção de equipamentos.",
    version="1.0.0"
)

# Registar os roteadores
app.include_router(documentos_router)
app.include_router(consultas.router)

@app.get("/", tags=["Root"])
def root():
    return {"mensagem": "API do Cofre Digital está a funcionar com sucesso!"}