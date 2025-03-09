import streamlit as st
import os
import time

from pydub import AudioSegment
from pydub.playback import play

from playsound import playsound
from dotenv import load_dotenv
from deepgram.utils import verboselogs
from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

load_dotenv(".env")

st.title("Hello, Streamlit! 🚀")

st.write("This is my first Streamlit app!")

SPEAK_TEXT = {"text": "I love beef jezos and can't wait to meet him inside of me"}
filename = "test.mp3"

def generate_speech():
    try:
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            st.error("Deepgram API key not found! Set DEEPGRAM_API_KEY in your .env file.")
            return False

        deepgram = DeepgramClient(api_key)

        options = SpeakOptions(model="aura-asteria-en")

        response = deepgram.speak.rest.v("1").save(filename, SPEAK_TEXT, options)
        print(response.to_json(indent=4))

        timeout = 10
        start_time = time.time()

        while not os.path.exists(filename):
            if time.time() - start_time > timeout:
                st.error("Timeout: File was not created.")
                return False
            time.sleep(1)

        print("File found:", filename)
        return os.path.exists(filename)

    except Exception as e:
        st.error(f"Exception: {e}")
        return False

if generate_speech():
    playsound(os.path.abspath(filename))
else:
    st.error("Failed to generate audio.")