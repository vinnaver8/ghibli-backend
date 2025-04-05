from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from stable_diffusion import generate_ghibli_image
import os

app = FastAPI()

# Enable CORS so your frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Testable root route
@app.get("/")
def read_root():
    return {"message": "Ghibli-style image backend is running!"}

# Image transform route
@app.post("/transform")
async def transform_image(file: UploadFile = File(...)):
    os.makedirs("temp", exist_ok=True)
    input_path = f"temp/{file.filename}"
    
    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Run transformation
    output_path = generate_ghibli_image(input_path)

    # Return transformed image
    return FileResponse(output_path, media_type="image/png", filename="ghibli_output.png")
