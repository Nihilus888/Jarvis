from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from models.prompt import PromptRequest
from services.deepseek_client import generate_text_with_deepseek
from routes.transcribe import transcribe_audio_file
from routes.text_to_speech import text_to_speech
from routes.logging_utils import log_interaction

router = APIRouter()

# POST /generate — Text input
@router.post("/generate")
def generate_text(req: PromptRequest):
    try:
        text = generate_text_with_deepseek(req.prompt)
        if not text:
            raise HTTPException(status_code=500, detail="Empty response from DeepSeek")
        text_to_speech(text, "response.mp3")
        return {"response": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/audio")
async def generate_from_audio(file: UploadFile = File(...)):
    try:
        transcription = transcribe_audio_file(file)
        response = generate_text_with_deepseek(transcription)
        Jarvis_response = text_to_speech(response, "response.mp3")
        log_interaction(response, Jarvis_response) 

        return FileResponse(
            path=Jarvis_response,
            media_type="audio/mpeg",
            filename="jarvis_response.mp3"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing error: {str(e)}")