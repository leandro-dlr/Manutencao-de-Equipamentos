import os
import hashlib
from core.logger import logger
from services.storage_service import ler_metadados
from core.config import config

def verificar_integridade_global():
    documentos = ler_metadados()
    dir_docs = config['storage']['diretorio_documentos']
    resultado = {"verificados": len(documentos), "integros": 0, "alterados": 0, "perdidos": 0}

    for doc in documentos:
        caminho = os.path.join(dir_docs, doc["nome_armazenado"])
        if not os.path.exists(caminho):
            resultado["perdidos"] += 1
            logger.warning(f"ARQUIVO_PERDIDO id={doc['id']}")
            continue
            
        sha256 = hashlib.sha256()
        with open(caminho, "rb") as f:
            for bloco in iter(lambda: f.read(4096), b""): 
                sha256.update(bloco)
            
        if sha256.hexdigest() == doc["sha256"]:
            resultado["integros"] += 1
        else:
            resultado["alterados"] += 1
            logger.error(f"INTEGRIDADE_FALHA id={doc['id']}")

    logger.info("VERIFICACAO_GLOBAL_CONCLUIDA")
    return resultado