import os
from google import genai
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

# Lê a chave de API
api_key = os.getenv("GOOGLE_API_KEY")

# Inicializa o cliente do Gemini
client = genai.Client(api_key=api_key)

# Faz uma pergunta para o modelo
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explique o que é RAG em poucas palavras."
)

# Mostra a resposta no terminal
print(response.text)