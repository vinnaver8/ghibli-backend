from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from stable_diffusion import generate_ghibli_image
import os

app = FastAPI()

# Add this for allowing GitHub Pages to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://vinnaver8.github.io"],  # Your GitHub Pages frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transform")
async def transform_image(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)  # Ensure temp folder exists

    input_path = f"temp/{file.filename}"
    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_path = generate_ghibli_image(input_path)
    return FileResponse(output_path, media_type="image/png", filename="ghibli_output.png")
