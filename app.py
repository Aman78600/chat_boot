import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import time
import threading

# Configure the Generative AI model
genai.configure(api_key='AIzaSyBgEWO0_xIuVPUWDQuQVvs8v3KtVHJY-7s')
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize the recognizer and microphone
r = sr.Recognizer()
my_mic = sr.Microphone(device_index=None)

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
    with my_mic as source:
        st.write("Say something...")
        audio = r.listen(source)
    
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
