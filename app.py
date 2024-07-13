import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import pyttsx3
import time
import threading
# from audiorecorder import audiorecorder

# Configure the Generative AI model
genai.configure(api_key='AIzaSyBgEWO0_xIuVPUWDQuQVvs8v3KtVHJY-7s')
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the recognizer and microphone
r = sr.Recognizer()
# mic_list = sr.Microphone.list_microphone_names()
# st.write("Available microphones:", mic_list)

# my_mic = 
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



# Function to convert text to speech using pyttsx3
def text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Change voice (experiment with indices)
    engine.setProperty('rate', 150)  # Adjust speaking speed (words per minute)
    engine.say(text)  # Speak the text
    engine.runAndWait()  # Process and play the speech

# Function to update Streamlit output in real-time
def speak_and_print(text_,question):
    st.write(question)
    output_placeholder = st.empty()

    t = ''
    for i in text_:
        t += i
        output_placeholder.write(t)
        time.sleep(0.05)
    output_placeholder.write('')
    st.write(text_)
    

# Streamlit button to trigger speech recognition and response generation
if st.button('Speak'):
    # with sr.Microphone(device_index=None) as source:
    st.write("Say something...")
        # audio = r.listen(source)
    if webrtc_ctx.audio_receiver:
        audio = webrtc_ctx.audio_receiver.get_frames(timeout=1)
    # audio=audio = audiorecorder("Click to record", "Click to stop recording")
    
    try:
        # Convert speech to text and generate response
        question = r.recognize_google(audio)
        response = model.generate_content('give me an answer in 40 to 80 words \nQuestion => ' + question).text
        
        # Start threading for text-to-speech and real-time text update
        tts_thread = threading.Thread(target=text_to_speech, args=(response,))
        tts_thread.start()

        speak_and_print(response,question)

        tts_thread.join()
        
    except sr.UnknownValueError:
        st.warning("Sorry, I couldn't understand what you said.")
