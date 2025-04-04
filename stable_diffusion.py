import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
from prompt_generator import generate_prompt

def generate_ghibli_image(image_path: str) -> str:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    ).to(device)

    init_image = Image.open(image_path).convert("RGB").resize((512, 512))
    prompt = generate_prompt(image_path) + ", ghibli style, animation look"

    output = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5)
    result = output.images[0]

    output_path = f"temp/ghibli_output.png"
    result.save(output_path)
    return output_path
