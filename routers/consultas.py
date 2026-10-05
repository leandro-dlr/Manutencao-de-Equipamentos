from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import csv
import io 

from repository import carregar_metadados

router = APIRouter()

#F2 - LISTAGEM GERAL
@router.get("/documentos")
def listar_documentos():
    dados = carregar_metadados()
    return dados

#F7 - FILTRAGEM COMBINADA
@router.get("/documentos/filtrar")
def filtrar_documentos(
    categoria: str | None = None,
    extensao: str | None = None,
    patrimonio: str | None = None,
    tecnico: str | None = None,
    tipo_manutencao: str | None = None,
):

    dados = carregar_metadados()

    resultado = []

    for documento in dados:
        passou = True # assume q o documento passa em todos os filtros

        if categoria is not None and documento.categoria != categoria:
            passou = False
        
        if extensao is not None and documento.extensao != extensao:
            passou = False

        if patrimonio is not None and documento.patrimonio != patrimonio:
            passou = False
        
        if tecnico is not None and documento.tecnico != tecnico:
            passou = False
        
        if tipo_manutencao is not None and documento.tipo_manutencao != tipo_manutencao:
            passou = False

        if passou:
            resultado.append(documento)

    if len(resultado) == 0:
        return {"mensagem": "Nenhum documento encontrado com os filtros aplicados"}

    return resultado


#F3 - CONSULTA POR ID
@router.get("/documentos/{id}")
def consultar_documentos(id: str):
    dados = carregar_metadados()
    
    for documento in dados:
        if documento.id == id:
            return documento

    raise HTTPException(status_code = 404, detail = "Documento não encontrado")

#F8 - ESTATÍSTICAS DO COFRE
@router.get("/estatísticas")
def estatisticas():
    dados = carregar_metadados()

    total_arquivos = len(dados)
    espaco_total = 0

    for documento in dados:
        espaco_total = espaco_total + documento.tamanho

    por_extensao = {}
    for documento in dados:
        extensao = documento.extensao
        if extensao in por_extensao:
            por_extensao[extensao] = por_extensao[extensao] + 1
        else:
            por_extensao[extensao] = 1

    por_tipo_manutencao = {}
    for documento in dados:
        tipo = documento.tipo_manutencao
        if tipo in por_tipo_manutencao:
            por_tipo_manutencao[tipo] = por_tipo_manutencao[tipo] + 1
        else:
            por_tipo_manutencao[tipo] = 1
        
    return {
        "total_arquivos": total_arquivos,
        "espaco_total_bytes": espaco_total,
        "distribuicao_por_extensao": por_extensao,
        "distribuicao_por_tipo_manutencao": por_tipo_manutencao,
    }

