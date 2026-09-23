from fastapi import FastAPI
from routers.documentos import router as documentos_router

app = FastAPI(
    title="Cofre Digital - Manutenção de Equipamentos",
    description="API para gestão de documentos e metadados de manutenção de equipamentos (Pessoa 1).",
    version="1.0.0"
)

# Registra o roteador criado da Pessoa 1
app.include_router(documentos_router)

@app.get("/", tags=["Root"])
def root():
    return {"mensagem": "API do Cofre Digital está rodando com sucesso!"}