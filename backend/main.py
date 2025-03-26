from fastapi import FastAPI
from pydantic import BaseModel
from backend.api_routes import router
import uvicorn
from backend.story_generator import generate_story, continue_story
import logging

app = FastAPI(title="AI Story Generator")
app.include_router(router)

class ImageCaptionRequest(BaseModel):
    image_caption: str

class ContinueStoryRequest(BaseModel):
    story: str
    user_choice: str

@app.get("/")
def home():
    return {"message": "Welcome to AI Story Generator API!"}

# ✅ Logging
logging.basicConfig(level=logging.INFO)

@app.post("/generate_story")
async def generate_story_endpoint(request: ImageCaptionRequest):
    logging.info(f"📝 Received request: {request}")
    return generate_story(request.image_caption)

@app.post("/continue_story")
async def continue_story_endpoint(request: ContinueStoryRequest):
    return continue_story(request.story, request.user_choice)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
