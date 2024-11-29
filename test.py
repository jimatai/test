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
        st.write("Saving...")
        with open("recorded_audio.wav", "wb") as f:
            f.write(audio_bytes)
        st.write("Recording saved!")
        st.success("Recording saved!")

        audio_file= open("./recorded_audio.wav", "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )

        st.write(transcription)

        speech_file_path = "recorded_audio.wav"
        response = client.audio.speech.create(
        model="tts-1",
        voice="fable", # alloy, echo, fable, onyx, nova, shimmer
        input= transcription
        )
        response.stream_to_file(speech_file_path)

        st.audio("recorded_audio.wav")

if __name__ == "__main__":
    main()