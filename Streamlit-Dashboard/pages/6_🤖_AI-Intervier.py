import os
import streamlit as st
import speech_recognition as sr
import pyttsx3
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Groq client
client = Groq(api_key=os.environ.get("VISION_API_KEY"))

# Streamlit Page Config
st.set_page_config(page_title="AI Voice Assistant", page_icon="🤖")

st.title("🤖 AI Voice Assistant")
st.markdown("Talk to your assistant like Alexa or Siri. Ask academic questions, schedule help, and more!")

# Text-to-Speech Engine
try:
    engine = pyttsx3.init()
    tts_available = True
except Exception:
    st.warning("⚠️ Text-to-Speech engine not available.")
    tts_available = False

def speak(text):
    if tts_available:
        engine.say(text)
        engine.runAndWait()
    else:
        st.info(f"(Voice): {text}")

# Speech Recognizer
recognizer = sr.Recognizer()

st.info("Click the button and speak your question...")

if st.button("🎙️ Start Listening"):
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            query = recognizer.recognize_google(audio)
            st.write(f"**You said:** `{query}`")

            # Call Groq API with user's voice input
            messages = [{"role": "user", "content": query}]

            with st.spinner("🤖 Thinking..."):
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    # model="llama-3-3b-8192",  # or "llama-3-3b-instruct" / "llama-3-70b"
                    model="llama-3.3-70b-versatile"
                )
                response = chat_completion.choices[0].message.content.strip()

            st.success(response)
            speak(response)

        except sr.WaitTimeoutError:
            st.error("⏱️ Listening timed out. Try again.")
        except sr.UnknownValueError:
            st.error("❓ Couldn't understand audio.")
        except sr.RequestError as e:
            st.error(f"🔌 Speech recognition error: {e}")
        except Exception as e:
            st.error(f"❌ Error: {e}")




# import streamlit as st
# import speech_recognition as sr
# import pyttsx3

# st.set_page_config(page_title="AI Voice Assistant", page_icon="🤖")

# st.title("🤖 AI Voice Assistant")
# st.markdown("Talk to your assistant like Alexa or Siri. Ask academic questions, scheduling help, and more!")

# # Initialize text-to-speech engine
# engine = pyttsx3.init()

# # Function to speak text
# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# # Speech-to-text (record input)
# recognizer = sr.Recognizer()

# st.info("Click the button and speak...")

# if st.button("🎙️ Start Listening"):
#     with sr.Microphone() as source:
#         st.write("Listening...")
#         audio = recognizer.listen(source)

#         try:
#             query = recognizer.recognize_google(audio)
#             st.write(f"You said: `{query}`")

#             # Placeholder AI response (simulate Grok)
#             response = f"Hello! You asked: {query}. (Imagine Grok's smart response here.)"

#             st.success(response)
#             speak(response)

#         except sr.UnknownValueError:
#             st.error("Sorry, I didn't catch that.")
#         except sr.RequestError as e:
#             st.error(f"Could not request results; {e}")
