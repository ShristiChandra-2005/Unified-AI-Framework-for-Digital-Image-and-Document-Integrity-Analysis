from pathlib import Path

from PIL import Image
from torchvision import transforms

from config.settings import IMAGE_SIZE, MEAN, STD
from utils.file_utils import validate_image_path


def load_rgb_image(image_path: str | Path) -> Image.Image:
    path = validate_image_path(image_path)
    return Image.open(path).convert("RGB")


def preprocess_for_model(image_path: str | Path):
    image = load_rgb_image(image_path)

    transform = transforms.Compose(
        [
            transforms.Resize(IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(mean=MEAN, std=STD),
        ]
    )

    tensor = transform(image).unsqueeze(0)
    return tensor, image
