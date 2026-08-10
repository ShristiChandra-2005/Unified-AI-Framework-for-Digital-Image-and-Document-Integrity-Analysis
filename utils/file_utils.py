import json
import pickle
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import torch

from config.settings import REPORTS_DIR, SUPPORTED_IMAGE_TYPES


def timestamp() -> str:
    """
    Human-readable timestamp for reports.
    Do not use this directly in filenames because it contains ':'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def file_timestamp() -> str:
    """
    Windows-safe timestamp for filenames.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def create_report_id(prefix: str) -> str:
    """
    Create a Windows-safe report ID.

    Example:
    module1_20260803_025147_a1b2c3d4
    """
    safe_prefix = (
        prefix.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )

    safe_time = file_timestamp()
    unique_id = uuid.uuid4().hex[:8]

    return f"{safe_prefix}_{safe_time}_{unique_id}"


def validate_image_path(image_path: str | Path) -> Path:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if path.suffix.lower() not in SUPPORTED_IMAGE_TYPES:
        raise ValueError(f"Unsupported image format: {path.suffix}")

    return path


def load_json(path: str | Path, default: Any = None) -> Any:
    path = Path(path)

    if not path.exists():
        return default

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data: Any, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False, default=str)

    return path


def save_json_report(data: dict[str, Any], report_id: str) -> Path:
    report_path = REPORTS_DIR / f"{report_id}.json"
    return save_json(data, report_path)


def save_prediction_report(data: dict[str, Any], module_prefix: str) -> tuple[str, Path]:
    report_id = create_report_id(module_prefix)
    report_path = save_json_report(data, report_id)
    return report_id, report_path


def load_pickle(path: str | Path, default: Any = None) -> Any:
    path = Path(path)

    if not path.exists():
        return default

    with path.open("rb") as file:
        return pickle.load(file)


def load_metadata(model_dir: str | Path) -> dict[str, Any]:
    model_dir = Path(model_dir)

    metadata_json = model_dir / "metadata.json"
    metadata_pkl = model_dir / "metadata.pkl"

    if metadata_json.exists():
        data = load_json(metadata_json, {})
        return data if isinstance(data, dict) else {}

    if metadata_pkl.exists():
        data = load_pickle(metadata_pkl, {})
        return data if isinstance(data, dict) else {}

    return {}


def load_checkpoint(path: str | Path, device: torch.device) -> dict[str, Any]:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {path}")

    checkpoint = torch.load(path, map_location=device)

    if isinstance(checkpoint, dict):
        return checkpoint

    return {"model_state_dict": checkpoint}


def extract_state_dict(checkpoint: dict[str, Any]) -> dict[str, Any]:
    return checkpoint.get("model_state_dict", checkpoint)


def load_class_names(path: str | Path, default: list[str]) -> list[str]:
    data = load_json(path, default)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return data.get("class_names", default)

    return default
