import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Load API key
load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def text_to_speech(text: str, output_path: str, voice: str = "JBFqnCBsd6RMkjVDRZzb") -> str:
    """
    Converts text to speech using ElevenLabs and saves the audio to a file.
    """
    audio_stream = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    # Write the full byte stream to file
    with open(output_path, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return output_path

# Test call
if __name__ == "__main__":
    text_to_speech("Hello, this is a test.", "output.mp3")