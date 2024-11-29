from openai import OpenAI
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from tempfile import NamedTemporaryFile

# Replace with your OpenAI API key
client = OpenAI(api_key= st.secrets["openai"]["api_key"])

# Example usage with Streamlit:
def main():
    st.title("Voice to Text Transcription")
    
    # Record audio using Streamlit widget
    audio_bytes = audio_recorder(pause_threshold=30)
    
    if st.button("Save Recording"):
        with open("recorded_audio.wav", "wb") as f:
            f.write(audio_bytes)
        st.success("Recording saved!")

        audio_file= open("./recorded_audio.wav", "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )

        st.write(transcription)

if __name__ == "__main__":
    main()