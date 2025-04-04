from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from stable_diffusion import generate_ghibli_image
import os

app = FastAPI()

@app.post("/transform")
async def transform_image(file: UploadFile = File(...)):
    input_path = f"temp/{file.filename}"
    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_path = generate_ghibli_image(input_path)
    return FileResponse(output_path, media_type="image/png", filename="ghibli_output.png")
