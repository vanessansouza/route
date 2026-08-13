from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from data import inicializar_base_vetorial
from prompt import SYSTEM_PROMPT

def criar_cadeia_rag():
    # Inicializa o retriever do Chroma
    retriever = inicializar_base_vetorial()

    # Configura o modelo LLM do Google
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)

    # Template do Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Com base exclusivamente nas diretrizes da Route fornecidas no contexto abaixo, responda à pergunta.\n\nContexto:\n{context}\n\nPergunta: {question}")
    ])

    # Montagem da Chain do LangChain (RAG)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
    