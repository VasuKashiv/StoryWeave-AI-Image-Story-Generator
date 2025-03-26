import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io

# ✅ Select best device
device = "cuda" if torch.cuda.is_available() else "cpu"

# ✅ Load BLIP captioning model
blip_model_id = "Salesforce/blip-image-captioning-base"
blip_processor = BlipProcessor.from_pretrained(blip_model_id, use_fast=False)
blip_model = BlipForConditionalGeneration.from_pretrained(blip_model_id).to(device)

async def analyze_image(file):
    """Processes an image and generates a caption using BLIP."""
    try:
        # ✅ Read and open image correctly from FastAPI's UploadFile object
        image_bytes = await file.read()  # Read file bytes
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # ✅ Prepare inputs for BLIP model
        inputs = blip_processor(images=image, return_tensors="pt").to(device)

        # ✅ Generate caption
        with torch.no_grad():
            caption_ids = blip_model.generate(**inputs, max_new_tokens=50)
            caption = blip_processor.batch_decode(caption_ids, skip_special_tokens=True)[0]
        return caption
    except Exception as e:
        print(f"❌ Error during image analysis: {str(e)}")
        return f"Error analyzing image: {str(e)}"
