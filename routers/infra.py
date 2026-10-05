from fastapi import APIRouter
from services.backup_service import criar_backup_geral, listar_arquivos_backup
from services.integrity_service import verificar_integridade_global

router = APIRouter()

@router.post("/backup")
def gerar_backup():
    return {"mensagem": "Backup criado com sucesso", "arquivo": criar_backup_geral()}

@router.get("/backups")
def listar_backups():
    return listar_arquivos_backup()

@router.get("/integridade")
def checar_integridade_global():
    return verificar_integridade_global()