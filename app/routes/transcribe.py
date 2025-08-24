# transcribe.py
import whisper
import os
import shutil

model = whisper.load_model("base")  # Load once globally

def transcribe_audio_file(upload_file):
    try:
        temp_path = f"temp_{upload_file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)

        result = model.transcribe(temp_path)
        os.remove(temp_path)
        return result['text']
    except Exception as e:
        raise RuntimeError(f"Transcription error: {str(e)}")