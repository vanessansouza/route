import streamlit as st
from dotenv import load_dotenv
from rag import criar_cadeia_rag

# Carrega variáveis de ambiente
load_dotenv()

# Configuração inicial da página
st.set_page_config(page_title="Route AI - Assistente Logístico", page_icon="🚚", layout="wide")

st.title("Olá!👋 Sou o **Route AI**")
st.markdown(
    "Consulte diretrizes operacionais, contratos, políticas de indenização e rastreabilidade da transportadora Route.\n\n"
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
    st.image("assets/logo-route.png", width=120)
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

 # PERGUNTAS SUGERIDAS FIXAS
    st.markdown("**💡 Perguntas Sugeridas**")
    
    pergunta_1 = "Quais são as condições gerais de frete?"
    pergunta_2 = "Como funciona o portal de rastreabilidade?"
    pergunta_3 = "Quais são os prazos de coleta, transferência e entrega?"
    pergunta_4 = "Quais são os canais oficiais de contato Route?"
    
    # Se o usuário clicar em qualquer botão, o texto é injetado automaticamente como prompt
    if st.button(pergunta_1, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": pergunta_1})
        with st.spinner("Buscando resposta..."):
            resposta = rag_chain.invoke(pergunta_1)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.rerun()
            
    if st.button(pergunta_2, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": pergunta_2})
        with st.spinner("Buscando resposta..."):
            resposta = rag_chain.invoke(pergunta_2)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.rerun()
            
    if st.button(pergunta_3, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": pergunta_3})
        with st.spinner("Buscando resposta..."):
            resposta = rag_chain.invoke(pergunta_3)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.rerun()
            
    if st.button(pergunta_4, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": pergunta_4})
        with st.spinner("Buscando resposta..."):
            resposta = rag_chain.invoke(pergunta_4)
            st.session_state.messages.append({"role": "assistant", "content": resposta})
            st.rerun()


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


