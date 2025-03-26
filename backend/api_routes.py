from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.image_analysis import analyze_image
from backend.story_generator import generate_story
import logging
from PIL import Image

router = APIRouter()
logging.basicConfig(level=logging.INFO)


@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """Handles image uploads, extracts captions, and generates a story."""
    try:
        image_caption = await analyze_image(file)
        logging.info(f"📝 Generated Caption: {image_caption}")  # Debugging

        if not image_caption:
            raise HTTPException(status_code=400, detail="Image analysis failed!")

        story = generate_story(image_caption)
        return {"caption": image_caption, "story": story}

    except Exception as e:
        logging.error(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing the image.")
