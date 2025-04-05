from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
from stable_diffusion import generate_ghibli_image

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ghibli backend is working!"}

@app.post("/transform")
async def transform_image(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)

    file_ext = os.path.splitext(file.filename)[-1]
    input_path = f"temp/input_{uuid.uuid4()}{file_ext}"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Call Stable Diffusion function
    output_path = generate_ghibli_image(input_path)

    return FileResponse(output_path, media_type="image/png", filename="ghibli_output.png")
