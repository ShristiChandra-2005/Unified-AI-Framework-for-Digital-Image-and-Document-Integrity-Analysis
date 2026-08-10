import torch.nn as nn
import torchvision.models as tv_models

try:
    import timm
except ImportError:
    timm = None


class BaselineCNN(nn.Module):
    def __init__(self, num_classes: int = 2) -> None:
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),

            nn.Conv2d(128, 256, 3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.35),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.25),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


def normalize_model_name(model_name: str | None) -> str:
    if not model_name:
        return "efficientnet"

    name = model_name.lower().replace("-", "_").replace(" ", "_")

    if "efficient" in name:
        return "efficientnet"

    if "xception" in name:
        return "xception"

    if "cnn" in name or "baseline" in name:
        return "cnn"

    return name


def build_model(model_name: str | None, num_classes: int) -> nn.Module:
    model_key = normalize_model_name(model_name)

    if model_key == "efficientnet":
        model = tv_models.efficientnet_b0(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
        return model

    if model_key == "xception":
        if timm is None:
            raise ImportError("Install timm first: pip install timm")

        return timm.create_model(
            "xception",
            pretrained=False,
            num_classes=num_classes,
        )

    if model_key == "cnn":
        return BaselineCNN(num_classes=num_classes)

    raise ValueError(f"Unsupported model architecture: {model_name}")
