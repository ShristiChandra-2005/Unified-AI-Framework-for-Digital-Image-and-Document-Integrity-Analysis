from typing import Any

import streamlit as st
import torch

from config.settings import DEVICE, MODELS_DIR
from models.architectures import build_model
from utils.file_utils import (
    extract_state_dict,
    load_checkpoint,
    load_class_names,
    load_json,
    load_metadata,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def _safe_load_state_dict(model: torch.nn.Module, state_dict: dict[str, Any]) -> str:
    try:
        model.load_state_dict(state_dict, strict=True)
        return "strict=True"

    except RuntimeError as error:
        logger.warning("strict=True failed. Using compatible fallback. Error: %s", error)

        model_state = model.state_dict()
        compatible_state = {}

        for key, value in state_dict.items():
            if key in model_state and model_state[key].shape == value.shape:
                compatible_state[key] = value

        if not compatible_state:
            raise RuntimeError("No compatible checkpoint weights found.")

        model_state.update(compatible_state)
        model.load_state_dict(model_state, strict=False)

        return f"strict=False | compatible_layers={len(compatible_state)}"


@st.cache_resource(show_spinner="Loading trained model...")
def load_trained_model(
    module_name: str,
    default_class_names: tuple[str, ...],
    default_model_name: str = "efficientnet",
) -> dict[str, Any]:
    """
    Load a trained PyTorch model once and reuse it across Streamlit reruns.

    This prevents repeated:
    - torch.load()
    - model building
    - checkpoint loading
    - state_dict loading

    Important:
    Do not cache prediction results here. Only cache reusable model resources.
    """

    model_dir = MODELS_DIR / module_name

    checkpoint_path = model_dir / "best_model.pth"
    config_path = model_dir / "config.json"
    class_path = model_dir / "class_names.json"

    class_names = load_class_names(class_path, list(default_class_names))
    config = load_json(config_path, {})
    metadata = load_metadata(model_dir)
    checkpoint = load_checkpoint(checkpoint_path, DEVICE)

    model_name = (
        checkpoint.get("model_name")
        or config.get("model_name")
        or metadata.get("model_name")
        or metadata.get("best_model")
        or default_model_name
    )

    model = build_model(model_name, len(class_names)).to(DEVICE)
    state_dict = extract_state_dict(checkpoint)
    load_mode = _safe_load_state_dict(model, state_dict)

    model.eval()

    logger.info(
        "%s loaded successfully | model=%s | mode=%s | device=%s",
        module_name,
        model_name,
        load_mode,
        DEVICE,
    )

    return {
        "model": model,
        "model_name": model_name,
        "class_names": class_names,
        "config": config,
        "metadata": metadata,
        "load_mode": load_mode,
        "checkpoint_path": checkpoint_path,
    }
