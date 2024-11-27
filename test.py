import openai
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from tempfile import NamedTemporaryFile

# Replace with your OpenAI API key
api_key = st.secrets["openai"]["api_key"]
openai.api_key = api_key

# Example usage with Streamlit:
def main():
    st.title("Voice to Text Transcription")
    
    # Record audio using Streamlit widget
    audio_bytes = audio_recorder(pause_threshold=30)
    
    if st.button("Save Recording"):
        with open("recorded_audio.wav", "wb") as f:
            f.write(audio_bytes)
        st.success("Recording saved!")

        audio_file = open("./recorded_audio.wav", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="vtt")

        st.write(transcript)

        with open("output.vtt", "w", encoding = "utf-8") as file:
            file.write(transcript)

if __name__ == "__main__":
    main()