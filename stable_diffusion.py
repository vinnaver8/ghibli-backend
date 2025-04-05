from diffusers import StableDiffusionImg2ImgPipeline
import torch
from PIL import Image
import os
import uuid

# Load model once
model_id = "nitrosocke/ghibli-diffusion"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
pipe.safety_checker = lambda images, **kwargs: (images, False)  # disable safety checker

def generate_ghibli_image(input_path):
    init_image = Image.open(input_path).convert("RGB").resize((512, 512))
    prompt = "ghibli style"
    strength = 0.75
    guidance_scale = 7.5

    output = pipe(prompt=prompt, image=init_image, strength=strength, guidance_scale=guidance_scale)
    result_image = output.images[0]

    output_path = f"temp/output_{uuid.uuid4()}.png"
    result_image.save(output_path)
    return output_path
