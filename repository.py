
import json
from pathlib import Path
from models import DocumentosManutencao

PASTA_RAIZ = Path(__file__).parent
CAMINHO_JSON = PASTA_RAIZ / "storage" / "metadata" / "documentos.json"


def carregar_metadados() -> list[DocumentosManutencao]:
    if not CAMINHO_JSON.exists():
        return []
    with open(CAMINHO_JSON, "r", encoding="utf-8") as f:
        dados_brutos = json.load(f)
    return [DocumentosManutencao(**item) for item in dados_brutos]
