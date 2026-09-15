from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class DocumentosManutencao(BaseModel):
    # Metadados Gerais
    id: str = Field(..., description="Identificador único do documento")
    nome_original: str = Field(..., description="Nome do arquivo enviado pelo usuário")
    nome_armazenado: str = Field(..., description="Nome gerado pelo sistema para salvar no disco")
    extensao: str = Field(..., description="Extensão do arquivo, ex: .pdf, .jpg")
    tipo_mime: str = Field(..., description="Tipo MIME, ex: application/pdf")
    tamanho: int = Field(..., description="Tamanho do arquivo em bytes")
    categoria: str = Field(..., description="Categoria geral do documento")
    descricao: Optional[str] = Field(None, description="Descrição do conteúdo do arquivo")
    data_upload: datetime = Field(default_factory=datetime.now, description="Data e hora do upload")
    sha256: str = Field(..., description="Hash SHA-256 para verificação de integridade")

    # Metadados específicos
    equipamento: str = Field(..., description="Nome ou tipo do equipamento. Ex: Torneadeira CNC")
    patrimonio: str = Field(..., description="Código de patrimônio. Ex: PAT-88392")
    tipo_manutencao: str = Field(..., description="Ex: Preventiva, Corretiva, Preditiva, Calibragem")
    tecnico: str = Field(..., description="Nome do técnico responsável")
    data_manutencao: date = Field(..., description="Data em que a manutenção ocorreu")

class DocumentoAtualizacao(BaseModel):
    # Modelo usado especificamente para a rota de PUT (Atualização)
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    equipamento: Optional[str] = None
    patrimonio: Optional[str] = None
    tipo_manutencao: Optional[str] = None
    tecnico: Optional[str] = None
    data_manutencao: Optional[date] = None