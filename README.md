# 🛡️ VeriShield AI
## Unified AI Framework for Digital Image and Document Integrity Analysis

VeriShield AI is an end-to-end AI-powered framework for analyzing the
authenticity and integrity of digital images and documents using Deep
Learning, Computer Vision, OCR, metadata analysis, and Explainable AI.

The framework combines multiple AI-based analysis modules into a unified
Streamlit application for detecting AI-generated images, identifying image
tampering, verifying digital receipts, and generating interpretable
integrity assessment reports.

---

## 🚀 Project Overview

The rapid growth of Generative AI and digital image-editing tools has made
it increasingly difficult to determine whether digital content is
authentic or manipulated.

Existing solutions often focus on a single type of digital content.
VeriShield AI provides a unified framework that combines multiple
analysis techniques to assess digital integrity.

The system currently supports:

- AI-generated image detection
- Image-tampering detection
- OCR-based receipt verification
- Metadata analysis
- Grad-CAM explainability
- Confidence-based prediction
- Risk assessment
- Automated JSON/PDF integrity reporting
- Interactive Streamlit-based analysis

---

## 🎯 Objectives

The main objectives of VeriShield AI are to:

- Detect AI-generated and synthetic images.
- Identify digitally manipulated or tampered images.
- Extract and analyze information from digital receipts.
- Validate available image and document metadata.
- Provide explainable visual evidence for model predictions.
- Combine model outputs into an interpretable integrity assessment.
- Provide an easy-to-use interface for digital content analysis.

---

# 🔍 Core Modules

## 1. AI-Generated Image Detection

This module classifies an uploaded image as either real or
AI-generated.

### Dataset

**CIFAKE**

### Models Evaluated

- CNN
- Xception
- EfficientNet-B0

### Best Experimental Result

- **Test Accuracy:** 98%
- **F1-Score:** 0.98
- **Best Model:** Xception

The module provides the predicted class and confidence score through the
Streamlit interface.

---

## 2. Image-Tampering Detection

This module analyzes images for signs of digital manipulation or tampering.

### Datasets

- CASIA v2
- IMD2020

### Model

**EfficientNet-B0**

### Experimental Result

- **Accuracy:** 83.47%
- **F1-Score:** 81.42%

The module provides a tampering prediction together with supporting
analysis and visual evidence.

---

## 3. Receipt Verification

The receipt verification module analyzes digital receipts using OCR and
document-processing techniques.

### Datasets

- SROIE
- CORD

### Capabilities

- OCR-based text extraction
- Receipt field analysis
- Document preprocessing
- Metadata analysis
- Integrity checks
- Risk assessment

The extracted information can be used to identify inconsistencies and
support receipt authenticity analysis.

---

## 4. Explainable AI with Grad-CAM

VeriShield AI integrates **Grad-CAM** to make deep-learning predictions
more interpretable.

Instead of showing only the final prediction, Grad-CAM produces a visual
representation of the image regions that contributed to the model's
decision.

This helps users understand the reasoning behind image-classification
results.

---

## 5. Metadata Analysis

The framework analyzes available metadata associated with uploaded files.

The analysis may include:

- Image format
- Image dimensions
- EXIF information
- Camera-related information
- Creation/modification information
- Available file properties

Metadata findings are used as additional integrity indicators alongside
the model prediction.

---

## 6. Risk & Integrity Assessment

The framework combines available analysis results to provide an overall
digital integrity assessment.

The analysis can include:

- Model prediction
- Confidence score
- Metadata findings
- OCR results
- Explainability information
- Integrity indicators
- Risk assessment

The objective is to provide users with evidence-based analysis rather
than relying only on a single prediction.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │      User Upload     │
                         │  Image / Receipt     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Streamlit App     │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
        │ AI-Generated   │ │ Receipt        │ │ Image          │
        │ Image          │ │ Verification   │ │ Tampering      │
        │ Detection      │ │                │ │ Detection      │
        └───────┬────────┘ └───────┬────────┘ └───────┬────────┘
                │                  │                  │
                ▼                  ▼                  ▼
        Deep Learning          OCR / NLP        Deep Learning
        CNN / Xception         SROIE / CORD     EfficientNet-B0
        EfficientNet-B0
                │                  │                  │
                └──────────────────┼──────────────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ Metadata Analysis    │
                        │ + Grad-CAM           │
                        │ + Risk Assessment    │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ Integrity Assessment │
                        │ & Evidence Report    │
                        └──────────────────────┘
