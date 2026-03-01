import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai

# --------- Initialize TTS -----------
engine = pyttsx3.init()

# --------- Streamlit UI -----------
st.title("Orion Voice Assistant")

user_name = "Vishal"  # ya dynamically change kar sakte ho
welcome_text = f"Welcome {user_name}!"
st.write(welcome_text)
engine.say(welcome_text)
engine.runAndWait()

# --------- Groq API Setup -----------
openai.api_key = "vishal"

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
if st.button("🎤 Speak Now"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            st.success(f"You said: {query}")
            
            response = call_groq_model(query)
            st.write(response)
            
            engine.say(response)
            engine.runAndWait()
            
        except Exception as e:
            st.error("Sorry, could not understand audio")