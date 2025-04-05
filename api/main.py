from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Ghibli backend is working!"}

@app.post("/ghibli-style/")
async def ghibli_style(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Dummy image-to-image step (replace with real model)
    output_image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # Save output for demonstration
    output_image.save("output.jpg")

    return JSONResponse(content={"status": "success", "detail": "Image processed and saved as output.jpg"})
