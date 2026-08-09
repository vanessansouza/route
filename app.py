import os
import asyncio

from google import genai
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Carrega as variáveis do .env
load_dotenv()

# Lê a chave de API
api_key = os.getenv("GOOGLE_API_KEY")

# Inicializa o cliente do Gemini
client = genai.Client(api_key=api_key)

# Lista dos 5 PDFs
caminhos_pdfs = [
    'documents/01_contratos_e_legal/condicoes_gerais_frete_route.pdf',
    'documents/02_tecnologia_e_rastreamento/portal_rastreabilidade_route.pdf',
    'documents/03_seguros_e_qualidade/politica_indenizacoes_route.pdf',
    'documents/04_atendimento_e_suporte/central_ajuda_route.pdf',
    'documents/04_atendimento_e_suporte/sac_ouvidoria_route.pdf'
    
]

async def criar_base_vetorial():
    todas_as_paginas = []
    
    # Carrega os PDFs
    print("Iniciando o carregamento dos PDFs...")
    for caminho in caminhos_pdfs:
        print(f"Carregando: {caminho}")
        loader = PyPDFLoader(caminho)
        async for page in loader.alazy_load():
            todas_as_paginas.append(page)
            
    print(f"Total de páginas carregadas: {len(todas_as_paginas)}")
    
    # Divide os textos em pedaços (Chunks)
    print("\nDividindo os textos em pedaços (chunks)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Tamanho máximo de cada pedaço em caracteres
        chunk_overlap=200  # Sobreposição para manter o contexto entre os pedaços
    )
    chunks = text_splitter.split_documents(todas_as_paginas)
    print(f"Total de pedaços (chunks) gerados: {len(chunks)}")
    
    # Configura o modelo de Embeddings do Google
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Cria e salva a Base de Dados Vetorial localmente (Chroma DB)
    print("\nCriando e salvando a base de dados vetorial (Chroma)...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db" # Pasta onde o banco vetorial será salvo
    )
    
    print("Base vetorial criada e salva com sucesso na pasta 'chroma_db'!")
    
    # Teste rápido de busca por similaridade
    pergunta_teste = "Qual é a política de indenizações para extravio?"
    print(f"\nTestando busca para a pergunta: '{pergunta_teste}'")
    
    resultados = vectorstore.similarity_search(pergunta_teste, k=2)
    print(f"Encontrados {len(resultados)} trechos relevantes nos PDFs:")
    for i, doc in enumerate(resultados):
        print(f"\n--- Trecho {i+1} (Fonte: {doc.metadata.get('source')}) ---")
        print(doc.page_content[:300] + "...")

# Executa o processo assíncrono
asyncio.run(criar_base_vetorial())