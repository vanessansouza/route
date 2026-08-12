import streamlit as st
from dotenv import load_dotenv
from rag import criar_cadeia_rag

# Carrega variáveis de ambiente
load_dotenv()

# Configuração inicial da página
st.set_page_config(page_title="Route AI - Assistente Logístico", page_icon="🚚", layout="wide")

st.title("Olá!👋 Sou o **Route AI**, seu assistente inteligente")
st.markdown(
    "Consulte diretrizes operacionais, contratos, políticas de indenização e rastreabilidade da Route.\n\n"
    "O que você gostaria de saber?"
)

# Inicializa a cadeia RAG de forma cacheada para otimizar performance
@st.cache_resource
def carregar_rag():
    return criar_cadeia_rag()

with st.spinner("Carregando base de conhecimento dos PDFs da Route..."):
    rag_chain = carregar_rag()

# Construção da Coluna Esquerda (Sidebar)
with st.sidebar:
    # Logo / Cabeçalho da Sidebar
    st.image("assets/imagem1.png", width=120)
    st.caption("Assistente Corporativo e Logístico")
    
    st.divider()
    
    # Seções / Áreas operacionais baseadas nos documentos
    st.markdown("**Áreas e Diretrizes**")
    st.markdown("""
    - Contratos & Jurídico
    - Tecnologia & Rastreamento
    - Seguros & Qualidade
    - Atendimento & Suporte (SAC)
    """)

    st.divider()

# Histórico de mensagens no chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto do usuário
if prompt := st.chat_input("Ex: Qual é a política de indenizações para extravio de cargas?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos da Route..."):
            try:
                resposta = rag_chain.invoke(prompt)
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
            except Exception as e:
                erro_msg = f"Ocorreu um erro ao processar sua pergunta: {e}"
                st.error(erro_msg)
