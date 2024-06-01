import torch
from diffusers import StableDiffusionPipeline
from GPUtil import showUtilization as gpu_usage
from numba import cuda
import os
import gc
import uuid  # Для генерации уникальных имен файлов


def free_gpu_cache():
    print("Initial GPU Usage")
    gpu_usage()

    torch.cuda.empty_cache()

    cuda.select_device(0)
    cuda.close()
    cuda.select_device(0)

    print("GPU Usage after emptying the cache")
    gpu_usage()


# Создание директории для сохранения изображений
os.makedirs("generated_images", exist_ok=True)

# Загрузка модели
model_id = "runwayml/stable-diffusion-v1-5"
device = "cuda" if torch.cuda.is_available() else "cpu"
if device == 'cuda':
    free_gpu_cache()

pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.to(device)


async def generate_image(text: str) -> str:
    image = pipe(text).images[0]
    unique_filename = f"{uuid.uuid4().hex}.png"  # Генерация уникального имени
    image_path = os.path.join("generated_images", unique_filename)
    image.save(image_path)
    return image_path
