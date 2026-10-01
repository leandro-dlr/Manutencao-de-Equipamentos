import json
from pathlib import Path 
from models import DocumentosManutencao

CAMINHO_JSON = Path("storage/metadata/documentos.json")


def carregar_metadados() -> list[DocumentosManutencao]:
    if not CAMINHO_JSON.exists():
        return []
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados_brutos = json.load(f)
    return[DocumentosManutencao(**item) for item in dados_brutos]
