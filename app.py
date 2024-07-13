import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from io import BytesIO

# Initialize recognizer
recognizer = sr.Recognizer()

st.title("Speech to Text with Streamlit")

# Record audio
audio = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording")
if audio:
    st.audio(audio, format='audio/wav')
    
    # Convert the recorded audio to a BytesIO object
    audio_data = BytesIO(audio.getvalue())
    
    # Use the recognizer to convert audio to text
    with sr.AudioFile(audio_data) as source:
        recorded_audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(recorded_audio)
            st.write("Text from audio:", text)
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
