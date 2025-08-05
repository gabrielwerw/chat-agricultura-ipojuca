import streamlit as st
import openai
from datetime import datetime

# Substitua pela sua chave real da OpenAI
openai.api_key = "sua_chave_aqui"

st.set_page_config(page_title="Secretaria da Agricultura Ipojuca", page_icon="🌾", layout="wide")

st.markdown("""
<style>
.user-msg {
    background-color: #DCF8C6;
    padding: 10px;
    border-radius: 10px;
    max-width: 80%;
    align-self: flex-end;
    margin: 5px;
}
.bot-msg {
    background-color: #F1F0F0;
    padding: 10px;
    border-radius: 10px;
    max-width: 80%;
    align-self: flex-start;
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Secretaria da Agricultura Ipojuca")

# Sugestão de cultivo por mês
def resposta_plantio_por_mes(pergunta):
    pergunta = pergunta.lower()
    palavras_chave = ["plantar", "plantio", "cultivar", "qual cultivo", "o que cultivo", "época de plantar"]
    if any(p in pergunta for p in palavras_chave):
        mes = datetime.now().month
        nomes_meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                       "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
        recomendacoes = {
            1: "milho, feijão, abóbora",
            2: "milho, batata-doce",
            3: "mandioca, melancia",
            4: "hortaliças, tomate",
            5: "pimentão, batata-doce",
            6: "couve, milho verde",
            7: "feijão, alface",
            8: "mandioca, batata-doce, feijão",
            9: "melancia, abobrinha",
            10: "milho, mandioca",
            11: "feijão, alface, cenoura",
            12: "batata, milho verde",
        }
        resposta = recomendacoes.get(mes, "Consulte um técnico local para orientação ideal.")
        return f"📅 Estamos em {nomes_meses[mes-1].capitalize()}. Em Ipojuca, este é um bom período para cultivar: **{resposta}**."
    return None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá, sou o assistente virtual da Secretaria da Agricultura de Ipojuca. Como posso te ajudar hoje?"}
    ]

# Mostrar histórico
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>👤 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# Entrada do usuário
prompt = st.chat_input("Digite sua pergunta...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    resposta_custom = resposta_plantio_por_mes(prompt)

    if resposta_custom:
        reply = resposta_custom
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message["content"]
        except Exception as e:
            reply = f"Erro ao conectar com a OpenAI: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()