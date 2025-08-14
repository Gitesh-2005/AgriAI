from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from gtts import gTTS
import os
import uuid

router = APIRouter()

@router.get("/tts")
async def text_to_speech(
    text: str = Query(..., description="Text to convert to speech"),
    lang: str = Query("en", description="Language code, e.g., 'en', 'hi', 'mr'")
):
    try:
        # Generate unique filename
        filename = f"speech_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("temp_audio", filename)
        
        # Ensure temp_audio folder exists
        os.makedirs("temp_audio", exist_ok=True)

        # Generate TTS audio
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)

        # Return the audio file
        return FileResponse(
            filepath,
            media_type="audio/mpeg",
            filename=filename,
            headers={"X-Audio-File": filename}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
