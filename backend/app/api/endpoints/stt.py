from fastapi import APIRouter, File, UploadFile, HTTPException
import os
from dotenv import load_dotenv
from groq import Groq

# Load env variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env.")

client = Groq(api_key=api_key)

router = APIRouter()

@router.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), language: str = None):
    """
    Accepts an audio file and returns the English translation using Groq Whisper.
    """
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # Use the correct endpoint (`translations`)
        with open(temp_path, "rb") as audio_file:
            translation = client.audio.translations.create(
                file=audio_file,
                model="whisper-large-v3",
                response_format="json",
                temperature=0.0,
                # language="en"  # Only 'en' is allowed for translation
            )

        os.remove(temp_path)  # Cleanup

        return {"translation": translation.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
