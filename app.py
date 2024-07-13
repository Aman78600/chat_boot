import streamlit as st
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import pyttsx3
import threading
import google.generativeai as genai

# Configure the Generative AI model
genai.configure(api_key='YOUR_API_KEY')  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to convert text to speech using pyttsx3
def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change voice (experiment with indices)
    engine.setProperty('rate', 150)  # Adjust speaking speed (words per minute)
    engine.say(text)  # Speak the text
    engine.runAndWait()  # Process and play the speech

# Function to update Streamlit output in real-time
def speak_and_print(response, question):
    st.write(f"Question: {question}")
    st.write(f"Response: {response}")
    st.write("Text-to-Speech:")
    text_to_speech(response)

# Streamlit button to trigger speech recognition and response generation
if st.button('Speak'):
    client_settings = ClientSettings(
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
    )

    # Capture audio from the microphone
    webrtc_ctx = webrtc_streamer(
        key="audio",
        mode=WebRtcMode.SENDRECV,
        client_settings=client_settings,
    )

    if webrtc_ctx.audio_receiver:
        audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        
        # Save audio frames to a file
        audio_path = "recorded_audio.wav"
        with open(audio_path, "wb") as f:
            f.write(b"".join([frame.to_ndarray() for frame in audio_frames]))

        # Recognize speech using SpeechRecognition
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
            question = r.recognize_google(audio_data)

        # Generate response from AI model
        response = model.generate_content(f"Give me an answer in 40 to 80 words.\nQuestion => {question}").text

        # Update Streamlit output with response and text-to-speech
        speak_and_print(response, question)
