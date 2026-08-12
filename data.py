import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# PDFs da Route
caminhos_pdfs = [
    'documents/01_contratos_e_legal/condicoes_gerais_frete_route.pdf',
    'documents/02_tecnologia_e_rastreamento/portal_rastreabilidade_route.pdf',
    'documents/03_seguros_e_qualidade/politica_indenizacoes_route.pdf',
    'documents/04_atendimento_e_suporte/central_ajuda_route.pdf',
    'documents/04_atendimento_e_suporte/sac_ouvidoria_route.pdf'
]

def inicializar_base_vetorial():
    todas_as_paginas = []
    
    # Carrega cada PDF local
    for caminho in caminhos_pdfs:
        if os.path.exists(caminho):
            loader = PyPDFLoader(caminho)
            paginas = loader.load()
            todas_as_paginas.extend(paginas)
        else:
            print(f"Aviso: Arquivo não encontrado em {caminho}")

    # Divide os textos em pedaços (Chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(todas_as_paginas)

    # Configura o modelo de Embeddings compatível do HuggingFace
    embeddings = HuggingFaceEmbeddings(model_name="mixedbread-ai/mxbai-embed-large-v1")

    # Criação e persistência do banco vetorial Chroma localmente
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    return vectorstore.as_retriever(search_kwargs={"k": 3})