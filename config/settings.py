from pathlib import Path

import torch

BASE_DIR = Path(__file__).resolve().parents[1]

MODELS_DIR = BASE_DIR / "models"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = OUTPUTS_DIR / "reports"
VISUALIZATIONS_DIR = OUTPUTS_DIR / "visualizations"
TEMP_DIR = OUTPUTS_DIR / "temp"
PREDICTIONS_DIR = OUTPUTS_DIR / "predictions"
DOWNLOADS_DIR = OUTPUTS_DIR / "downloads"

for folder in [
    OUTPUTS_DIR,
    REPORTS_DIR,
    VISUALIZATIONS_DIR,
    TEMP_DIR,
    PREDICTIONS_DIR,
    DOWNLOADS_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMAGE_SIZE = (224, 224)
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

SUPPORTED_IMAGE_TYPES = [
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
]
