from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import replicate
import os
import uuid

app = FastAPI()

# Allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_99dQLOHAPr8dvnfrxuOuZbZmMzJfDD11icXnP"

@app.get("/")
def root():
    return {"message": "ghibli backend is working!"}

@app.post("/transform")
async def transform_image(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    input_path = f"temp/{uuid.uuid4().hex}_{file.filename}"
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Upload image to Replicate and run model
    with open(input_path, "rb") as img_file:
        output = replicate.run(
            "tstramer/realistic-vision-v5.1:db21e45c324a93e0a2d71cb9634fae63b6eeabf77e6993eb1a7a5edc3f6c6a1c",
            input={
                "image": img_file,
                "prompt": "ghibli style, fantasy background, magical lighting, detailed scene",
                "guidance_scale": 7.5,
                "num_inference_steps": 30,
                "scheduler": "K_EULER"
            }
        )

    return JSONResponse({"image_url": output})
