from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from datetime import date, datetime
import os

from models import DocumentoAtualizacao, DocumentosManutencao
from services.storage_service import ler_metadados, salvar_metadados, calcular_hash_arquivo

router = APIRouter()

DIR_DOCUMENTOS = "./storage/documentos"

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=DocumentosManutencao)
async def upload_documento(
    categoria: str = Form(...),
    descricao: str = Form(...),
    equipamento: str = Form(...),
    patrimonio: str = Form(...),
    tipo_manutencao: str = Form(...),
    tecnico: str = Form(...),
    data_manutencao: date = Form(...),
    arquivo: UploadFile = File(...)
):
    conteudo = await arquivo.read()
    if not conteudo:
        raise HTTPException(status_code=400, detail="Arquivo vazio não é permitido.")

    tamanho = len(conteudo)
    sha256 = calcular_hash_arquivo(conteudo)

    documentos = ler_metadados()

    max_id = max([int(doc['id']) for doc in documentos if doc["id"].isdigit()], default=0)
    novo_id = str(max_id + 1)

    nome_original = arquivo.filename
    extensao = os.path.splitext(nome_original)[1].lower()
    nome_armazenado = f"{novo_id}{extensao}"
    caminho_salvamento = os.path.join(DIR_DOCUMENTOS, nome_armazenado)

    os.makedirs(DIR_DOCUMENTOS, exist_ok=True)
    with open(caminho_salvamento, 'wb') as f:
        f.write(conteudo)

    novo_doc = {
        "id": novo_id,
        "nome_original": nome_original,
        "nome_armazenado": nome_armazenado,
        "extensao": extensao,
        "tipo_mime": arquivo.content_type or "application/octet-stream",
        "tamanho": tamanho,
        "categoria": categoria,
        "descricao": descricao,
        "equipamento": equipamento,
        "patrimonio": patrimonio,
        "tipo_manutencao": tipo_manutencao,
        "tecnico": tecnico,
        "data_manutencao": data_manutencao.isoformat(),
        "data_upload": datetime.now().isoformat(),
        "sha256": sha256
    }
    documentos.append(novo_doc)
    salvar_metadados(documentos)

    return novo_doc

@router.get("/{id}/download")
def download_documento(id: str):
    documentos = ler_metadados()
    doc = next((doc for doc in documentos if doc["id"] == id), None)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")

    caminho_arquivo = os.path.join(DIR_DOCUMENTOS, doc["nome_armazenado"])
    if not os.path.exists(caminho_arquivo):
        raise HTTPException(status_code=404, detail="Arquivo físico não encontrado.")

    return FileResponse(caminho_arquivo, media_type=doc["tipo_mime"], filename=doc["nome_original"])

@router.put("/{id}", response_model=DocumentosManutencao)
async def atualizar_documento(id: str, dados_atualizacao: DocumentoAtualizacao):
    documentos = ler_metadados()
    doc_index = next((i for i, d in enumerate(documentos) if str(d["id"]) == str(id)), None)

    if doc_index is None:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")

    doc_atual = documentos[doc_index]
    campos_alterados =  dados_atualizacao.model_dump(exclude_unset=True)

    for campo, valor in campos_alterados.items():
        if valor is not None:
            if isinstance(valor, date):
                doc_atual[campo] = valor.isoformat()
            else:
                doc_atual[campo] = valor

    documentos[doc_index] = doc_atual
    salvar_metadados(documentos)

    return doc_atual

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def deletar_documento(id: str):
    documentos = ler_metadados()
    doc = next((d for d in documentos if str(d["id"]) == str(id)), None)

    if not doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado.")

    caminho_arquivo = os.path.join(DIR_DOCUMENTOS, doc["nome_armazenado"])
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)

    novos_documentos = [d for d in documentos if str(d["id"]) != str(id)]
    salvar_metadados(novos_documentos)

    return {"mensagem": f"Documento {id} e seu arquivo físico deletados com sucesso."}