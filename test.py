from openai import OpenAI
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from tempfile import NamedTemporaryFile

from google.oauth2 import service_account
from google.cloud import dialogflow_v2beta1 as dialogflow
import json
import uuid

# Replace with your OpenAI API key
client = OpenAI(api_key="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")

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

        dialogflow_credential_path = 'smart-pxud-8e8de1cea674.json'
        with open(dialogflow_credential_path, 'r') as f:
            service_account_info = json.load(f)

        session_id = uuid.uuid4()
        location = 'asia-northeast1'

        credential = service_account.Credentials.from_service_account_info(service_account_info)
        session_client = dialogflow.SessionsClient(credentials=credential, client_options={'api_endpoint': '%s-dialogflow.googleapis.com:443' % (location,)})
        project_id = '%s/locations/%s' % (service_account_info['project_id'], location,)
        session_path = session_client.session_path(project=project_id, session=session_id)

        question = transcription

        text_input = dialogflow.TextInput(text=question, language_code='ja')
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session_path, "query_input": query_input}
        )

        response_text = response.query_result.fulfillment_messages[0].text.text[0]

        speech_file_path = "recorded_audio.wav"
        response = client.audio.speech.create(
        model="tts-1",
        voice="fable", # alloy, echo, fable, onyx, nova, shimmer
        input= response_text
        )
        response.stream_to_file(speech_file_path)

        st.write(response_text)

        st.audio("recorded_audio.wav")

if __name__ == "__main__":
    main()