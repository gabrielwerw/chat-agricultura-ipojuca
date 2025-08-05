import streamlit as st
import openai

st.set_page_config(page_title="Secretaria da Agricultura Ipojuca")

st.title("🤖 Secretaria da Agricultura Ipojuca")
st.markdown("☁️ Olá, sou o assistente virtual da Secretaria da Agricultura de Ipojuca. Como posso te ajudar hoje?")

# Campo de entrada do usuário
user_input = st.chat_input("Digite sua pergunta...")

# Chave segura do arquivo .streamlit/secrets.toml
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Histórico
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Processar nova mensagem
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                temperature=0.7,
            )
            reply = response.choices[0].message["content"]
        except Exception as e:
            reply = f"⚠️ Erro ao conectar com a OpenAI: {str(e)}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})