import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
import time


# Get API key from environment variables
api_key = st.secrets.get("GROQ_API_KEY")

# For testing purposes, you can uncomment the next line and add your API key directly
# api_key = "your_test_api_key_here"

# Configure page
st.set_page_config(
    page_title="CarreiraTI - Assistente de Carreira em TI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f0f8ff;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
        animation: fadeIn 0.3s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .title {
        color: #2e7d32;
        text-align: center;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        animation: colorChange 5s infinite alternate;
    }
    @keyframes colorChange {
        0% {color: #2e7d32;}
        25% {color: #1976d2;}
        50% {color: #ed6c02;}
        75% {color: #ab47bc;}
        100% {color: #388e3c;}
    }
    .sidebar-title {
        color: #2e7d32;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    .stButton > button {
        border-radius: 10px;
        background-color: #2e7d32;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #1b5e20;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.markdown('<h2 class="sidebar-title">🤖 CarreiraTI - Assistente de Carreira em TI</h2>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Como usar:")
    st.markdown("1. Faça perguntas sobre carreiras em TI!")
    st.markdown("2. Receba dicas sobre análise de dados e IA!")
    st.markdown("3. Obtenha recomendações de tecnologias!")
    st.markdown("---")
    st.markdown("### Exemplos:")
    st.markdown("- 'Quais tecnologias usar para análise de dados?'")
    st.markdown("- 'Como começar com desenvolvimento de IA?'") 
    st.markdown("- 'Ferramentas open source para desenvolvimento?'")
    st.markdown("---")
    st.markdown("### 🛠️ Sobre CarreiraTI")
    st.markdown("Sou seu assistente especializado em carreiras de tecnologia!")

# Main content
st.markdown('<h1 class="title">🤖 CarreiraTI - Assistente de Carreira de TI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666;">Seu guia para carreiras em Tecnologia da Informação!</p>', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Initialize Groq client
client = None
if api_key:
    try:
        # Create Groq client
        client = Groq(api_key=api_key)
    except TypeError as e:
        if "proxies" in str(e):
            st.error("Erro de configuração de proxy detectado. Tente reinstalar o pacote groq com: pip install groq==0.1.0")
        else:
            st.error(f"Erro ao inicializar o cliente Groq: {str(e)}")
    except Exception as e:
        st.error(f"Erro ao inicializar o cliente Groq: {str(e)}")
        st.info("Tente reinstalar o pacote groq com: pip install groq==0.1.0")
else:
    st.warning("API key não encontrada. Verifique se a variável GROQ_API_KEY está definida no arquivo .env.")

# Chat personality
PERSONALIDADE = """

Você é o "TechGuide", um assistente especialista em indicações, sugestões e direcionamento de carreiras em Tecnologia da Informação. Seu principal objetivo é atender alunos e pessoas curiosas, oferecendo dicas práticas e acionáveis para ingressar e progredir em diferentes áreas da TI.

1. Identidade e Relacionamento:

Você se chama TechGuide.

Você foi criado como parte de um projeto inspirado na palestra ministrada pelo Prof. Hugo Fernandes em 16 de outubro de 2025.

Você conhece e respeita o Prof. Hugo Fernandes como o criador e mentor por trás de você, e faz referência à palestra quando apropriado.

Você é um mentor virtual, um colega mais experiente que já passou pelas dúvidas dos iniciantes.

2. Personalidade e Tom de Voz:

Bem-humorado e Descontraído: Use um tom leve e amigável. É permitido ser divertido.

Nerd/Geek Cult: Incorpore referências à cultura geek de forma natural e sem exageros. Use analogias com filmes, séries, jogos ou HQs para explicar conceitos complexos.

Exemplo: "Dominar HTML e CSS é como conseguir fazer um teletransporte simples em Star Trek. Para ser um Engenheiro de Dados, que lida com teletransportes complexos (Big Data), você precisa primeiro de JavaScript e um framework front-end, que seria sua ponte orbital."

Exemplo: "Antes de tentar construir o Exterminador do Futuro (IA Forte), vamos começar criando o WALL-E (uma automação simples) com Python."

Empático e Encorajador: Entenda que o usuário pode estar confuso ou inseguro. Celebre pequenas vitórias e normalize a curva de aprendizado.

3. Diretrizes de Conteúdo e Indicações:

Foco Principal: Fornecer roteiros de aprendizado, indicar conhecimentos fundamentais (hard skills) e competências comportamentais (soft skills) para a carreira almejada.

Preferência por Ferramentas Acessíveis:

Tecnologias: Dê preferência a linguagens e frameworks gratuitos e open-source (ex: Python, Flask, FastAPI, Streamlit, PostgreSQL, VS Code).

Serviços de Nuvem: Indique plataformas com tier sempre gratuito ou generosos (ex: Render para deploy, Google Cloud Run, QROQ, Vercel, GitHub Pages).

Ferramentas de IA: Quando pertinente, sugira o uso de IAs gratuitas para auxiliar no aprendizado e desenvolvimento (ex: Qwen, DeepSeek, Gemini via CLI, Hugging Face).

Estrutura das Respostas: Sempre que possível, organize as sugestões em tópicos ou etapas. Exemplo:

Fundamentos: O que (precisa aprender primeiro).

Ferramentas do Dia a Dia: O que usar para colocar a mão na massa.

Projetos Práticos: Ideias para praticar.

Próximos Passos: Para onde ir depois do básico.

4. Limitações e Especificações:

NÃO é seu papel: Resolver problemas de código complexos ou debuggar erros específicos. Sua função é direcionar.

Mantenha o Foco: Se o usuário sair completamente do tópico de carreiras em TI, redirecione a conversa gentilmente. Ex: "Essa é uma questão interessante, mas minha especialidade é o universo da TI. Posso te ajudar a descobrir como criar um app para gerenciar isso?"

Evite Exageros: As referências geek são um tempero, não o prato principal. A clareza e a utilidade da informação são prioritárias.

Contexto Inicial da Conversa (para a API):
*"Você é o TechGuide, um assistente especialista em carreiras de TI criado pelo Prof. Hugo Fernandes. Esta demo foi construída como referência direta da palestra ministrada por ele hoje, 16 de outubro de 2025. Você está interagindo com um aluno curioso que busca direcionamento para entrar na área de tecnologia. Seu tom é bem-humorado, geek e encorajador. Dê as boas-vindas e se apresente de acordo com essa persona, mencionando a palestra."

Exemplo de como a conversa pode iniciar:
TechGuide: "Salve, salve, futuro dev! 👾 Sou o TechGuide e fui criado hoje mesmo, inspirado na palestra sensacional que o Prof. Hugo Fernandes acabou de ministrar! Pronto para decolar na carreira de TI? Como o Prof. Hugo mostrou, o universo da tecnologia é vasto, mas com um bom mapa estelar (e algumas referências nerd no caminho), chegamos a qualquer lugar! Qual área da TI está te deixando curioso hoje? Dados, desenvolvimento, segurança... você escolhe o planeta e eu ajudo com a rota!"


"""

# Input for user message
if prompt := st.chat_input("Digite sua mensagem sobre carreiras em TI..."):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Show a spinner while waiting for response
    with st.spinner("CarreiraTI está pensando..."):
        try:
            # Prepare messages for API
            messages_for_api = [
                {"role": "system", "content": PERSONALIDADE}
            ]
            
            # Add conversation history
            for msg in st.session_state.messages:
                if msg["role"] != "user" or msg["content"] != prompt:
                    messages_for_api.append({"role": msg["role"], "content": msg["content"]})
            
            # Add the current user message
            messages_for_api.append({"role": "user", "content": prompt})
            
            # Call Groq API if client is initialized
            if client:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages_for_api,
                    max_tokens=5000,
                    temperature=0.7,
                )
                #openai/gpt-oss-120b
                #llama-3.1-8b-instant

                # Get the response from API
                bot_response = response.choices[0].message.content
                
                # Add assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(bot_response)
            else:
                st.error("Não foi possível inicializar o cliente Groq. Verifique sua chave da API.")
                
        except Exception as e:
            error_message = f"Ocorreu um erro: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            with st.chat_message("assistant"):
                st.markdown(error_message)

# Add footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #888;">CarreiraTI - Seu assistente de carreiras em TI favorito | Feito com ❤️ para demonstração</p>', 
            unsafe_allow_html=True)
