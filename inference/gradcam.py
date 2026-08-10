from pathlib import Path

import cv2
import numpy as np
import torch
import torch.nn as nn
from PIL import Image

from config.settings import DEVICE, VISUALIZATIONS_DIR
from utils.file_utils import file_timestamp


class GradCAM:
    """
    Generic Grad-CAM implementation for CNN/EfficientNet/Xception-style models.
    """

    def __init__(self, model: nn.Module, target_layer: nn.Module) -> None:
        self.model = model
        self.target_layer = target_layer
        self.gradients: torch.Tensor | None = None
        self.activations: torch.Tensor | None = None

        self.forward_hook = target_layer.register_forward_hook(self._save_activation)
        self.backward_hook = target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input_tensor, output_tensor) -> None:
        self.activations = output_tensor.detach()

    def _save_gradient(self, module, grad_input, grad_output) -> None:
        self.gradients = grad_output[0].detach()

    def generate(self, input_tensor: torch.Tensor, class_index: int) -> np.ndarray:
        self.model.eval()
        self.model.zero_grad(set_to_none=True)

        output = self.model(input_tensor)
        score = output[:, class_index]
        score.backward(retain_graph=True)

        if self.gradients is None or self.activations is None:
            raise RuntimeError("Grad-CAM failed to capture gradients or activations.")

        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self.activations).sum(dim=1).squeeze()
        cam = torch.relu(cam).detach().cpu().numpy()

        cam = cv2.resize(cam, (224, 224))
        cam = cam - cam.min()
        cam = cam / (cam.max() + 1e-8)

        return cam

    def remove_hooks(self) -> None:
        self.forward_hook.remove()
        self.backward_hook.remove()


def find_target_layer(model: nn.Module) -> nn.Module:
    conv_layers = [
        module for module in model.modules()
        if isinstance(module, nn.Conv2d)
    ]

    if not conv_layers:
        raise RuntimeError("No convolution layer found for Grad-CAM.")

    return conv_layers[-1]


def save_gradcam_overlay(
    model: nn.Module,
    input_tensor: torch.Tensor,
    original_image: Image.Image,
    class_index: int,
    image_stem: str,
    prefix: str,
) -> Path:
    """
    Generate and save Grad-CAM overlay image.

    Returns:
        Path of saved visualization.
    """
    VISUALIZATIONS_DIR.mkdir(parents=True, exist_ok=True)

    target_layer = find_target_layer(model)
    gradcam = GradCAM(model, target_layer)

    try:
        cam = gradcam.generate(input_tensor.to(DEVICE), class_index)
    finally:
        gradcam.remove_hooks()

    image = np.array(original_image.resize((224, 224)).convert("RGB"))

    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    overlay = cv2.addWeighted(image, 0.60, heatmap, 0.40, 0)

    safe_name = f"{prefix}_{image_stem}_{file_timestamp()}.png"
    output_path = VISUALIZATIONS_DIR / safe_name

    cv2.imwrite(str(output_path), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

    return output_path
