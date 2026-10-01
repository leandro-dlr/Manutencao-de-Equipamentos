import json
import os
import hashlib

METADATA_PATH = "./storage/metadata/documentos.json"

def ler_metadados():
    if not os.path.exists(METADATA_PATH):
        return []
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        try: 
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_metadados(metadados):
    os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadados, f, ensure_ascii=False, indent=4)

def calcular_hash_arquivo(conteudo_bytes):
    return hashlib.sha256(conteudo_bytes).hexdigest()
