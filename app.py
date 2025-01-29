import streamlit as st
import textwrap
from groq import Groq

# Streamlit App Title
st.title("Audio Transcription with Groq")

st.write("Upload an audio file, and the app will transcribe it.")

# Load API Key from Streamlit Secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except KeyError:
    st.error("API key is missing! Please add 'GROQ_API_KEY' to Streamlit Secrets.")

# File Upload
uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

# If file is uploaded
if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    st.audio(uploaded_file, format="audio/mp3")

    # Button for transcription
    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            try:
                # Send audio file to Groq API
                transcription = client.audio.transcriptions.create(
                    file=(uploaded_file.name, uploaded_file.read()),
                    model="whisper-large-v3",
                    response_format="verbose_json",
                )
                st.success("Transcription completed!")

                # Display the transcribed text
                st.text_area("Transcription Result", "\n".join(textwrap.wrap(transcription.text, width=120)), height=300)

            except Exception as e:
                st.error(f"An error occurred: {e}")
