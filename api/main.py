from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from stable_diffusion import generate_ghibli_image
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transform")
async def transform_image(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    input_path = f"temp/{file.filename}"
    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_path = generate_ghibli_image(input_path)
    return FileResponse(output_path, media_type="image/png", filename="ghibli_output.png")

# Vercel needs this line:
# This exposes the FastAPI app as "app" for ASGI
app = app
