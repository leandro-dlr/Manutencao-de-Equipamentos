from fastapi import FastAPI 
from routers import consultas 

app = FastAPI(title = "Cofre Digital de Arquivos - Manutenção de equipamentos")

app.include_router(consultas.router)

#testep