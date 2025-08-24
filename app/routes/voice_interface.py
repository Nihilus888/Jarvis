import pvporcupine
import pyaudio
import struct
import wave
import requests
import time
import os
import pygame  # ✅ Replaces pydub for audio playback
from dotenv import load_dotenv

# Constants
WAKE_WORD = "jarvis"
AUDIO_FILENAME = "user_input.wav"
MP3_FILENAME = "jarvis_response.mp3"
RECORD_SECONDS = 5
API_ENDPOINT = "http://localhost:8000/generate/audio"


# Initialize pygame mixer
pygame.mixer.init()

load_dotenv()

PICO_KEY = os.getenv("PICO_KEY")
if not PICO_KEY:
    raise ValueError("PICO_KEY environment variable is not set. Please set it in your .env file.")


def listen_for_wake_word():
    porcupine = pvporcupine.create(access_key=PICO_KEY, keywords=[WAKE_WORD])
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    print("🎤 Say 'Hey Jarvis' to begin...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            if porcupine.process(pcm):
                print("🟢 Wake word detected!")
                break
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()


def record_audio(filename=AUDIO_FILENAME, seconds=RECORD_SECONDS):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    print(f"🎧 Recording for {seconds} seconds...")

    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                     input=True, frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("✅ Recording saved.")


def play_mp3(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"🔴 Failed to play audio: {e}")


def send_audio_to_api(audio_path=AUDIO_FILENAME):
    print("📡 Sending audio to FastAPI backend...")
    with open(audio_path, "rb") as f:
        files = {"file": (audio_path, f, "audio/wav")}
        response = requests.post(API_ENDPOINT, files=files)

    if response.status_code == 200:
        with open(MP3_FILENAME, "wb") as out:
            out.write(response.content)
            if not os.path.exists(MP3_FILENAME):
                print("🔴 MP3 file not found!")
                return

        print("🔊 Response received. Playing now...")
        play_mp3(MP3_FILENAME)
    else:
        print("❌ Error:", response.status_code, response.text)


def main_loop():
    while True:
        listen_for_wake_word()
        record_audio()
        send_audio_to_api()
        print("⏳ Ready for next interaction...")
        time.sleep(1)


if __name__ == "__main__":
    main_loop()
