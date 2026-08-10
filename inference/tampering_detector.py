from pathlib import Path
from time import perf_counter
from typing import Any

import streamlit as st
import torch
import torch.nn.functional as F

from inference.gradcam import save_gradcam_overlay
from preprocessing.tampering_preprocessing import preprocess_for_tampering_model
from utils.file_utils import create_report_id
from utils.helper import (
    confidence_label,
    generate_tampering_summary,
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

MODULE_NAME = "Module 3 - Image Tampering Detection"


class TamperingDetector:
    def __init__(self) -> None:
        loaded = load_trained_model(
            module_name="module3",
            default_class_names=("Authentic", "Tampered"),
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

            tensor, image = preprocess_for_tampering_model(image_path)
            device = next(self.model.parameters()).device
            tensor = tensor.to(device)

            with torch.no_grad():
                outputs = self.model(tensor)
                probabilities_tensor = F.softmax(outputs, dim=1)[0]
                confidence_tensor, predicted_index = torch.max(
                    probabilities_tensor,
                    dim=0,
                )

            class_index = int(predicted_index)
            raw_prediction = self.class_names[class_index]
            prediction = _normalize_tampering_label(raw_prediction)
            confidence = round(float(confidence_tensor.item()) * 100, 2)

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
                        prefix="module3_tampering_gradcam",
                    )
                except Exception as error:
                    visualization_error = str(error)
                    logger.warning("Module 3 Grad-CAM failed: %s", error)

            processing_time_ms = round((perf_counter() - start_time) * 1000, 2)

            probabilities = _normalize_probabilities(
                class_names=self.class_names,
                probabilities_tensor=probabilities_tensor,
            )

            tampering_details = _build_tampering_details(
                prediction=prediction,
                confidence=confidence,
                risk_level=risk_level,
                gradcam_path=gradcam_path,
            )

            decision_summary = generate_tampering_summary(
                prediction=prediction,
                confidence=confidence,
                risk_level=risk_level,
                gradcam_path=str(gradcam_path) if gradcam_path else None,
                visualization_error=visualization_error,
            )

            report_id = create_report_id("module3")

            model = build_model_info(
                name=str(self.model_name),
                version=self.config.get(
                    "model_version",
                    self.metadata.get("model_version", "N/A"),
                ),
                dataset=self.config.get(
                    "dataset",
                    self.metadata.get("dataset", "CASIA v2 + IMD2020"),
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

            report["raw_prediction"] = raw_prediction
            report["manipulation_status"] = tampering_details["manipulation_status"]
            report["tampering_type"] = tampering_details["tampering_type"]
            report["affected_region"] = tampering_details["affected_region"]
            report["localization_status"] = tampering_details["localization_status"]
            report["heatmap_status"] = tampering_details["heatmap_status"]
            report["recommendation"] = tampering_details["recommendation"]
            report["details"] = tampering_details

            save_report(report)
            log_prediction(logger, report)

            return report

        except Exception as error:
            logger.exception("Module 3 prediction failed")
            return build_error_report(
                module=MODULE_NAME,
                image_path=image_path,
                error=error,
            )


def _normalize_tampering_label(label: str) -> str:
    label_lower = str(label).lower().strip()

    tampered_words = [
        "fake",
        "tampered",
        "manipulated",
        "forged",
        "splice",
        "spliced",
        "copy",
        "copy-move",
        "tp",
        "positive",
    ]

    authentic_words = [
        "real",
        "authentic",
        "original",
        "genuine",
        "normal",
        "au",
        "negative",
    ]

    if any(word in label_lower for word in tampered_words):
        return "Tampered"

    if any(word in label_lower for word in authentic_words):
        return "Authentic"

    return "Tampered" if label_lower == "1" else "Authentic"


def _normalize_probabilities(
    class_names: list[str],
    probabilities_tensor: torch.Tensor,
) -> dict[str, float]:
    probabilities = {
        "Authentic": 0.0,
        "Tampered": 0.0,
    }

    for index, class_name in enumerate(class_names):
        normalized_label = _normalize_tampering_label(class_name)
        probability = round(float(probabilities_tensor[index].item()) * 100, 2)

        probabilities[normalized_label] = max(
            probabilities.get(normalized_label, 0.0),
            probability,
        )

    return probabilities


def _build_tampering_details(
    prediction: str,
    confidence: float,
    risk_level: str,
    gradcam_path: Path | None,
) -> dict[str, Any]:
    if prediction == "Tampered":
        if confidence >= 90:
            tampering_type = "Strong suspected manipulation"
            affected_region = "High-confidence manipulated region highlighted in heatmap"
        elif confidence >= 75:
            tampering_type = "Possible image manipulation"
            affected_region = "Suspicious region highlighted in heatmap"
        else:
            tampering_type = "Weak manipulation indication"
            affected_region = "Low-confidence suspicious region"

        recommendation = (
            "Manual forensic verification recommended before using this image "
            "as trusted digital evidence."
        )
    else:
        tampering_type = "No clear manipulation detected"
        affected_region = "No suspicious region detected"
        recommendation = "Image appears authentic based on current model output."

    if gradcam_path:
        localization_status = "Available"
        heatmap_status = "Displayed below"
    else:
        localization_status = "Unavailable"
        heatmap_status = "Localization unavailable"

    return {
        "manipulation_status": prediction,
        "prediction": prediction,
        "confidence": confidence,
        "tampering_type": tampering_type,
        "affected_region": affected_region,
        "localization_status": localization_status,
        "heatmap_status": heatmap_status,
        "risk_level": risk_level,
        "recommendation": recommendation,
    }


@st.cache_resource(show_spinner="Preparing tampering detector...")
def get_tampering_detector() -> TamperingDetector:
    """
    Cache detector instance so model is not reloaded on every prediction.
    """

    return TamperingDetector()


def predict_tampering(image_path: str | Path) -> dict[str, Any]:
    detector = get_tampering_detector()
    return detector.predict(image_path)
