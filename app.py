import os
import asyncio
from google import genai
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

# Carrega as variáveis do .env
load_dotenv()

# Lê a chave de API
api_key = os.getenv("GOOGLE_API_KEY")

# Inicializa o cliente do Gemini
client = genai.Client(api_key=api_key)

#Faz uma pergunta baseada no conteúdo real dos seus PDFs (ex: sobre indenizações ou frete)
pergunta_desafio = "Qual é a política de indenizações para casos de extravio de cargas?"

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=f"Com base na pergunta '{pergunta_desafio}', prepare a resposta para o usuário."
)

# Mostra a resposta no terminal
print(response.text)

# Lista com os caminhos relativos dos seus PDFs na estrutura do projeto
caminhos_pdfs = [
    'documents/01_contratos_e_legal/condicoes_gerais_frete_route.pdf',
    'documents/02_tecnologia_e_rastreamento/portal_rastreabilidade_route.pdf',
    'documents/03_seguros_e_qualidade/politica_indenizacoes_route.pdf',
    'documents/04_atendimento_e_suporte/central_ajuda_route.pdf',
    'documents/04_atendimento_e_suporte/sac_ouvidoria_route.pdf'
    
]

async def carregar_pdfs():
    todas_as_paginas = []
    
    for caminho in caminhos_pdfs:
        print(f"Carregando: {caminho}")
        loader = PyPDFLoader(caminho)
        
        # Mantém exatamente a mesma lógica assíncrona que você gostou
        async for page in loader.alazy_load():
            todas_as_paginas.append(page)
            
    print(f"\nTotal de páginas carregadas de todos os PDFs: {len(todas_as_paginas)}")
    
    if todas_as_paginas:
        print(f"\nMetadados da 1ª página: {todas_as_paginas[0].metadata}\n")
        print(f"Conteúdo:\n{todas_as_paginas[0].page_content[:300]}...")

# Executa a função assíncrona de carregamento dos PDFs
asyncio.run(carregar_pdfs())