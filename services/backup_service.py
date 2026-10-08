import os
import shutil
from datetime import datetime
from core.config import config
from core.logger import logger

def criar_backup_geral():
    dir_docs = config['storage']['diretorio_documentos']
    dir_backups = config['storage']['diretorio_backups']
    os.makedirs(dir_backups, exist_ok=True)
    
    nome_backup = f"backup_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    shutil.make_archive(os.path.join(dir_backups, nome_backup), "zip", dir_docs)
    
    logger.info(f"BACKUP_CRIADO arquivo={nome_backup}.zip")
    return f"{nome_backup}.zip"

def listar_arquivos_backup():
    dir_backups = config['storage']['diretorio_backups']
    if not os.path.exists(dir_backups): 
        return []
        
    return [{"arquivo": f, "tamanho": os.path.getsize(os.path.join(dir_backups, f))} 
            for f in os.listdir(dir_backups) if f.endswith(".zip")]