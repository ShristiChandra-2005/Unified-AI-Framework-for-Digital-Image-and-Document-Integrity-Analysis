from pathlib import Path
from time import perf_counter
from typing import Any

import streamlit as st
import torch
import torch.nn.functional as F

from inference.gradcam import save_gradcam_overlay
from preprocessing.image_preprocessing import preprocess_for_model
from utils.file_utils import create_report_id
from utils.helper import (
    confidence_label,
    generate_ai_summary,
    get_risk_level_and_score,
)
from utils.logger import get_logger, log_prediction
from utils.model_loader import load_trained_model
from utils.report_builder import (
    build_error_report,
    build_model_info,
    build_prediction_report,
    build_processing_info,
    build_visualization_info,
    save_report,
)

logger = get_logger(__name__)

MODULE_NAME = "Module 1 - AI Generated Image Detection"


class AIImageDetector:
    def __init__(self) -> None:
        loaded = load_trained_model(
            module_name="module1",
            default_class_names=("FAKE", "REAL"),
            default_model_name="efficientnet",
        )

        self.model = loaded["model"]
        self.model_name = loaded["model_name"]
        self.class_names = loaded["class_names"]
        self.config = loaded["config"]
        self.metadata = loaded["metadata"]
        self.load_mode = loaded["load_mode"]

    def predict(
        self,
        image_path: str | Path,
        generate_gradcam: bool = True,
    ) -> dict[str, Any]:
        try:
            start_time = perf_counter()

            tensor, image = preprocess_for_model(image_path)

            device = next(self.model.parameters()).device
            tensor = tensor.to(device)

            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities_tensor = F.softmax(outputs, dim=1)[0]
                confidence_tensor, predicted_index = torch.max(
                    probabilities_tensor,
                    dim=0,
                )

            confidence = round(float(confidence_tensor.item()) * 100, 2)
            class_index = int(predicted_index)
            prediction = self.class_names[class_index]

            risk_level, risk_score = get_risk_level_and_score(
                prediction=prediction,
                confidence=confidence,
            )

            gradcam_path = None
            visualization_error = None

            if generate_gradcam:
                try:
                    gradcam_path = save_gradcam_overlay(
                        model=self.model,
                        input_tensor=tensor,
                        original_image=image,
                        class_index=class_index,
                        image_stem=Path(image_path).stem,
                        prefix="module1_gradcam",
                    )
                except Exception as error:
                    visualization_error = str(error)
                    logger.warning("Module 1 Grad-CAM failed: %s", error)

            processing_time_ms = round((perf_counter() - start_time) * 1000, 2)

            probabilities = {
                self.class_names[index]: round(
                    float(probabilities_tensor[index].item()) * 100,
                    2,
                )
                for index in range(len(self.class_names))
            }

            decision_summary = generate_ai_summary(
                prediction=prediction,
                confidence=confidence,
                risk_level=risk_level,
                gradcam_path=str(gradcam_path) if gradcam_path else None,
                visualization_error=visualization_error,
            )

            report_id = create_report_id("module1")

            model = build_model_info(
                name=str(self.model_name),
                version=self.config.get(
                    "model_version",
                    self.metadata.get("model_version", "N/A"),
                ),
                dataset=self.config.get(
                    "dataset",
                    self.metadata.get("dataset", "CIFAKE"),
                ),
                accuracy=self.config.get(
                    "accuracy",
                    self.metadata.get("accuracy", "N/A"),
                ),
                precision=self.config.get(
                    "precision",
                    self.metadata.get("precision", "N/A"),
                ),
                recall=self.config.get(
                    "recall",
                    self.metadata.get("recall", "N/A"),
                ),
                f1_score=self.config.get(
                    "f1_score",
                    self.metadata.get("f1_score", "N/A"),
                ),
            )

            processing = build_processing_info(
                time_ms=processing_time_ms,
                image_path=image_path,
            )

            visualization = build_visualization_info(
                gradcam_path=str(gradcam_path) if gradcam_path else None,
                overlay_path=str(gradcam_path) if gradcam_path else None,
                error=visualization_error,
            )

            report = build_prediction_report(
                module=MODULE_NAME,
                image_path=image_path,
                prediction=prediction,
                confidence=confidence,
                confidence_label_value=confidence_label(confidence),
                risk_level=risk_level,
                risk_score=risk_score,
                decision_summary=decision_summary,
                model=model,
                processing=processing,
                visualization=visualization,
                probabilities=probabilities,
                report_id=report_id,
                model_load_mode=self.load_mode,
            )

            save_report(report)
            log_prediction(logger, report)

            return report

        except Exception as error:
            logger.exception("Module 1 prediction failed")
            return build_error_report(
                module=MODULE_NAME,
                image_path=image_path,
                error=error,
            )


@st.cache_resource(show_spinner="Preparing AI image detector...")
def get_ai_image_detector() -> AIImageDetector:
    """
    Cache detector instance so model is not reloaded on every prediction.
    """

    return AIImageDetector()


def predict_ai_image(image_path: str | Path) -> dict[str, Any]:
    detector = get_ai_image_detector()
    return detector.predict(image_path)
