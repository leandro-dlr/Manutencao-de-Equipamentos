import os
import hashlib
from core.logger import logger
from services.storage_service import ler_metadados
from core.config import config

def verificar_integridade_por_id(id_documento: str):
    documentos = ler_metadados()
    # Procura o documento específico
    doc = next((d for d in documentos if d["id"] == id_documento), None)
    
    if not doc:
        return {"erro": "Documento não encontrado."}

    dir_docs = config['storage']['diretorio_documentos']
    caminho = os.path.join(dir_docs, doc["nome_armazenado"])
    
    if not os.path.exists(caminho):
        logger.warning(f"ARQUIVO_PERDIDO id={id_documento}")
        return {"id": id_documento, "status": "perdido"}
        
    sha256 = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""): 
            sha256.update(bloco)
            
    if sha256.hexdigest() == doc["sha256"]:
        return {"id": id_documento, "status": "integro"}
    else:
        logger.error(f"INTEGRIDADE_FALHA id={id_documento}")
        return {"id": id_documento, "status": "alterado"}

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