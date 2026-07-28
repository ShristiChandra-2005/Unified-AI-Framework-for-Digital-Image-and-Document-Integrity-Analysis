# 🛡️ Unified AI Framework for Digital Image and Document Integrity Analysis

An end-to-end AI framework that verifies the authenticity and integrity of digital images and documents using Deep Learning, OCR, metadata analysis, and Explainable AI.

This project integrates multiple AI techniques into a single platform capable of detecting AI-generated images, identifying digitally manipulated images, verifying receipt authenticity, and producing an interpretable integrity assessment report.

---

# 🚀 Project Overview

The rapid growth of Generative AI and image editing tools has made it increasingly difficult to determine whether digital content is authentic.

Most existing solutions focus on only one task, such as:

- AI-generated image detection
- Receipt OCR
- Image tampering detection

This project combines these capabilities into a unified AI framework that automatically selects the appropriate analysis pipeline based on the uploaded content and provides a comprehensive integrity assessment.

---

# ✨ Features

- 🤖 AI-Generated Image Detection
- 🖼️ Digital Image Tampering Detection
- 🧾 Receipt Verification using OCR
- 📊 Metadata Analysis
- 🔍 Explainable AI using Grad-CAM
- 📄 Automatic PDF Report Generation
- 🎯 Integrity & Confidence Assessment
- 🌐 Interactive Streamlit Dashboard

---

# 🏗️ System Architecture

```
                 User
                   │
                   ▼
          Streamlit Dashboard
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
 AI Image      Receipt     Image
 Detection    Verification Tampering
        │          │          │
 EfficientNet  EasyOCR   EfficientNet
        │          │          │
        └──────────┼──────────┘
                   ▼
        Explainability Engine
                   ▼
    Integrity Assessment Engine
                   ▼
      PDF Analysis Report
```

---

# 📦 Project Modules

## 1. AI Image Detection

Detects whether an uploaded image is:

- Real
- AI Generated

### Model

- EfficientNet-B0

### Dataset

- CIFAKE

### Output

- Prediction
- Confidence Score
- Grad-CAM Visualization

---

## 2. Receipt Verification

Extracts and verifies information from receipts using OCR.

### Model

- EasyOCR

### Datasets

- SROIE
- CORD

### Output

- Extracted Text
- Merchant Name
- Date
- Amount
- OCR Confidence
- Metadata Analysis
- Integrity Assessment

---

## 3. Digital Image Tampering Detection

Detects manipulated or edited images.

### Model

- EfficientNet-B0

### Datasets

- CASIA v2
- IMD2020

### Output

- Original / Tampered
- Confidence Score
- Grad-CAM Visualization

---

## 4. Explainability Engine

Provides transparent explanations for AI predictions.

### Uses

- Grad-CAM for image models
- OCR output interpretation
- Metadata validation

---

## 5. Integrity Assessment Engine

Combines outputs from all modules to generate a final integrity assessment.

### Output

- Integrity Score
- Confidence Score
- Final Assessment
- Explainable Report

---

# 🔄 Workflow

```
User Uploads Image / Receipt
            │
            ▼
System Identifies Content Type
            │
            ▼
Run AI Model / OCR Pipeline
            │
            ▼
Generate Prediction
            │
            ▼
Explain Prediction
            │
            ▼
Integrity Assessment
            │
            ▼
Generate PDF Report
```

---

# 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Deep Learning | PyTorch |
| Computer Vision | OpenCV |
| OCR | EasyOCR |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib |
| Explainability | Grad-CAM |
| Dashboard | Streamlit |
| Development | Jupyter Notebook, VS Code |
| Report Generation | ReportLab |

---

# 📂 Project Structure

```
Unified-AI-Framework/

│── datasets/
│── notebooks/
│── models/
│── reports/
│── outputs/
│── images/

│── ai_image_detection/
│── receipt_verification/
│── image_tampering/
│── explainability/
│── integrity_engine/

│── app.py
│── requirements.txt
│── README.md
│── LICENSE
```

---

# 🚀 Installation

```bash
git clone https://github.com/yourusername/Unified-AI-Framework.git

cd Unified-AI-Framework

pip install -r requirements.txt

streamlit run app.py
```

---

# 🎯 Expected Outcomes

- Detect AI-generated images
- Detect digitally manipulated images
- Verify receipts using OCR
- Explain AI predictions with Grad-CAM
- Generate an integrity assessment report
- Produce downloadable PDF reports

---

# 📈 Future Improvements

- Support additional document formats
- Multi-language OCR
- Real-time API deployment
- Cloud deployment (AWS/Azure)
- Mobile application integration
- Vision Transformer (ViT) models
- LLM-based document reasoning

---

# 👩‍💻 Author

**Shristi Chandra**

B.Tech – Computer Science & Engineering (Artificial Intelligence)

Indira Gandhi Delhi Technical University for Women (IGDTUW)

---

# 📜 License

This project is licensed under the MIT License.
