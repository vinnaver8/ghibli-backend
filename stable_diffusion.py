from diffusers import StableDiffusionPipeline
import torch

def generate_ghibli_image(input_path):
    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4", 
        torch_dtype=torch.float32
    )
    pipe = pipe.to("cpu")

    image = pipe(prompt="ghibli style", image=input_path).images[0]
    output_path = "temp/ghibli_output.png"
    image.save(output_path)
    return output_path
