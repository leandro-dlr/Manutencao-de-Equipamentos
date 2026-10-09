# Cofre Digital de Arquivos - Gestao de Documentacao de Manutencao (FastAPI)

Este repositorio contem a implementacao do sistema Cofre Digital de Arquivos, desenvolvido em Python com o framework FastAPI para a disciplina de Desenvolvimento de Software para Persistencia (UFC Quixada)[cite: 1].

O sistema e focado na persistencia nativa em arquivos (JSON, CSV, YAML, logs e binarios) sem o uso de bancos de dados relacionais (SGBDs), sendo especializado na gestao, rastreabilidade e auditoria de documentos de manutencao de equipamentos industriais[cite: 1].

---

## Visao Geral do Sistema

O Cofre Digital oferece uma solucao centralizada para o gerenciamento do ciclo de vida de documentos tecnicos de ativos industriais (manuais em PDF, fotos de avarias em imagens, relatorios de inspecao e dados de sensores em CSV)[cite: 1]. O sistema garante a persistencia dos arquivos fisicos no disco local e a manipulacao estruturada de seus metadados, alem de prover mecanismos para auditoria de integridade, exportacao de dados, geracao de backups compactados e relatorios analiticos do historico dos equipamentos[cite: 1, 2, 3].

---

## Modelo de Dados e Metadados do Dominio

O modelo de dados Pydantic do sistema combina atributos padrao de gerenciamento de arquivos com metadados obrigatorios especificos do dominio de manutencao industrial[cite: 1]:

- id: Identificador unico do documento no cofre[cite: 1].
- nome_original: Nome do arquivo enviado pelo usuario[cite: 1].
- nome_armazenado: Nome unico utilizado para salvar o arquivo no disco local[cite: 1].
- extensao: Extensao do arquivo (ex: .pdf, .png, .csv)[cite: 1].
- tipo_mime: Tipo de media do arquivo (ex: application/pdf, image/png)[cite: 1].
- tamanho: Tamanho do arquivo em bytes[cite: 1].
- categoria: Categoria funcional do documento (ex: Manual, Relatorio, Fotos)[cite: 1].
- descricao: Descricao detalhada do conteudo do arquivo[cite: 1].
- data_upload: Data e hora em que o registro foi inserido no sistema[cite: 1].
- sha256: Hash SHA-256 gerado no upload para verificacao de integridade[cite: 1].
- equipamento: Nome ou identificacao do ativo industrial (ex: Torneadeira CNC 02)[cite: 1].
- patrimonio: Codigo unico de patrimonio do equipamento (ex: PAT-88392)[cite: 1].
- tipo_manutencao: Classificacao da intervencao (ex: Preventiva, Corretiva, Preditiva, Calibragem)[cite: 1].
- tecnico: Nome do profissional responsavel pela manutencao[cite: 1].
- data_manutencao: Data da realizacao da intervencao tecnica[cite: 1].

---

## Funcionalidades do Sistema

O sistema disponibiliza um conjunto unificado de recursos acessiveis por rotas HTTP da API:

### Gestao de Arquivos e Metadados
- Upload de Arquivos: Recebimento de arquivos binarios e metadados tecnicos, com geracao automatica de hash SHA-256, armazenamento no disco e persistencia dos metadados em JSON[cite: 2].
- Download de Arquivos: Recuperacao e envio do arquivo original armazenado, preservando a integridade binaria, o nome original e o tipo MIME[cite: 2].
- Atualizacao de Metadados: Alteracao dos dados descritivos e tecnicos do registro sem afetar o arquivo fisico correspondente[cite: 2].
- Exclusao de Documentos: Remocao completa do registro no arquivo JSON e eliminacao do arquivo fisico do disco[cite: 2].

### Consultas, Filtros e Relatorios
- Listagem Geral: Consulta paginada e navegavel de todos os documentos cadastrados no sistema[cite: 2].
- Consulta por ID: Localizacao detalhada dos metadados de um documento especifico atraves do seu identificador[cite: 2].
- Filtragem Combinada: Pesquisa avancada de documentos utilizando multiplos criterios simultaneos (por patrimonio, tecnico, tipo de manutencao, categoria ou extensao)[cite: 2].
- Estatisticas do Cofre: Calculo e exibicao de metricas consolidadas sobre o uso de espaco em disco, distribuicao de extensoes e contagem por tipo de manutencao[cite: 2].
- Exportacao do Catalogo: Exportacao de todo o catalogo de metadados para formato CSV[cite: 2].
- Dossie de Vida Util do Patrimonio: Relatorio analitico consolidado do historico do equipamento (endpoint GET /equipamentos/{patrimonio}/dossie), compilando historico de intervencoes, lista de tecnicos atuantes, proporcao entre manutencoes preventivas e corretivas e a data da ultima ocorrencia.

### Confiabilidade, Seguranca e Infraestrutura
- Verificacao de Integridade Individual: Checagem de integridade de um arquivo especifico recalculando o seu hash SHA-256 no disco e comparando com o hash gravado no JSON[cite: 2].
- Verificacao de Integridade Global: Varredura e auditoria completa de todos os arquivos armazenados no cofre digital[cite: 2].
- Sistema Centralizado de Logging: Registro sistematico de operacoes, acessos e falhas em niveis INFO, WARNING e ERROR[cite: 2].
- Configuracao Externa: Carregamento de parametros globais do sistema via arquivo de configuracao YAML[cite: 2].
- Sistema de Backup Compactado: Geracao de arquivos de backup no formato ZIP contendo os binarios e o arquivo de metadados JSON[cite: 2].
- Gestao de Backups: Listagem e consulta dos arquivos de backup criados no sistema[cite: 2].
- Tratamento de Excecoes: Padronizacao de respostas de erro e codigos HTTP adequados para requisicoes invalidas ou recursos nao encontrados[cite: 2].

---

## Tecnologias Utilizadas

- FastAPI: Framework web em Python de alto desempenho para criacao de APIs RESTful[cite: 1].
- Pydantic: Biblioteca para validacao e estruturacao de dados e metadados[cite: 1].
- Uvicorn: Servidor ASGI para execucao da aplicacao.
- hashlib: Biblioteca nativa para calculo de hashes SHA-256 e auditoria de integridade[cite: 2].
- PyYAML: Manipulacao de arquivos de configuracao no formato YAML[cite: 2].
- JSON / CSV / ZIP: Formatos nativos de arquivos utilizados para persistencia de metadados, exportacao de dados e compactacao de backups[cite: 1, 2].

---

## Estrutura de Diretorios do Projeto

```text
├── core/                       # Modulos centrais da aplicacao
│   ├── config.py              # Leitura de configuracoes externas (YAML)
│   ├── integrity.py           # Utilitarios de verificacao de integridade SHA-256
│   └── logger.py              # Configuracao do sistema centralizado de logs
├── routers/                    # Endpoints e rotas HTTP da API
│   ├── consultas.py           # Rotas de listagem, filtros, estatisticas e dossie
│   ├── documentos.py          # Rotas de upload, download, edicao e exclusao
│   └── infra.py               # Rotas de integridade, logs, configuracao e backup
├── services/                   # Camada de regras de negocio
│   ├── backup_service.py      # Criacao e gestao de backups ZIP
│   ├── integrity_service.py   # Auditoria global e individual de hashes
│   └── storage_service.py     # Gestao de ficheiros binarios e persistencia JSON
├── storage/                    # Camada de armazenamento fisico
│   ├── documentos/            # Diretorio onde sao salvos os ficheiros binarios
│   └── metadata/              # Ficheiro documentos.json para metadados
├── main.py                     # Ponto de entrada da aplicacao FastAPI
├── models.py                   # Modelos Pydantic (DocumentosManutencao)
├── repository.py               # Camada de abstracao para leitura/escrita em disco
├── catalogo.csv                # Ficheiro exportado com o catalogo do cofre
├── config.yaml                 # Ficheiro YAML de configuracao externa
├── requirements.txt            # Dependencias do projeto
└── .gitignore                  # Ficheiros ignorados pelo versionamento


## Como Executar o Projeto Localmente

### 1. Pre-requisitos
Certifique-se de ter o Python 3.10+ e o Git instalados em seu sistema.

### 2. Clonar o Repositorio
git clone <URL_DO_REPOSITORIO>
cd cofre-digital

### 3. Criar e Ativar o Ambiente Virtual
No Windows (Command Prompt ou PowerShell):
python -m venv venv
.\venv\Scripts\activate

No Linux / macOS:
python3 -m venv venv
source venv/bin/activate

### 4. Instalar as Dependencias
pip install -r requirements.txt

### 5. Executar a Aplicacao
uvicorn main:app --reload