import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import openai
import os
import tempfile

# --------- Streamlit UI -----------
st.title("Orion Voice Assistant")

# User name
user_name = "Vishal"  # ya dynamically set kar sakte ho
welcome_text = f"Welcome {user_name}!"
st.write(welcome_text)

# --------- Groq/OpenAI API Setup -----------
openai.api_key = st.secrets.get("GROQ_API_KEY", "your_default_key_here")

def call_groq_model(query):
    response = openai.ChatCompletion.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are Orion, a helpful assistant."},
            {"role": "user", "content": query}
        ]
    )
    return response['choices'][0]['message']['content']

# --------- Voice Input Button -----------
st.write("Click 🎤 and speak your query:")

if st.button("🎤 Speak Now"):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = r.listen(source)
            query = r.recognize_google(audio)
            st.success(f"You said: {query}")
            
            # Call Orion
            response_text = call_groq_model(query)
            st.write(response_text)
            
            # Generate TTS using gTTS
            tts = gTTS(text=response_text, lang='en')
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
            st.audio(temp_file.name)
            
    except Exception as e:
        st.error(f"Audio error or recognition failed: {e}")

# --------- Optional: Text Input Fallback -----------
query_text = st.text_input("Or type your query here:")

if query_text:
    response_text = call_groq_model(query_text)
    st.write(response_text)
    
    tts = gTTS(text=response_text, lang='en')
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    st.audio(temp_file.name)
