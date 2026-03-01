import streamlit as st
import requests

# 🔑 Apni Groq API Key yaha daalo
API_KEY = "vishal"

URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

st.set_page_config(page_title="Orion AI", page_icon="🤖")
st.title("🤖 Orion AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Orion, a smart and helpful AI assistant."}
    ]

# Display previous chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    data = {
       "model": "llama-3.1-8b-instant",
        "messages": st.session_state.messages
    }

    response = requests.post(URL, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        reply = result["choices"][0]["message"]["content"]
    else:
        reply = "⚠️ Error: " + str(result)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.write(reply)