VeriShield AI: An Integrated Framework for Digital Content Integrity Analysis
AI-generated image detection · Receipt verification · Image tampering detection

VeriShield AI is a research-oriented prototype that combines computer vision, optical character recognition (OCR), image classification, and rule-based validation to analyze the integrity of digital images and document content. The system brings three complementary analysis modules into one application to help users examine potentially AI-generated images, verify extracted receipt information, and identify images that may contain manipulations.
Research status: Prototype under evaluation. The reported results are preliminary and require further reproducibility checks. VeriShield AI provides analytical signals to support human review; it does not guarantee authenticity or establish fraud conclusively.

Table of Contents
- Overview
- Key Features
- System Architecture
- Module 1: AI-Generated Image Detection
- Module 2: Receipt Verification
- Module 3: Image Tampering Detection
- Datasets
- Evaluation Methodology
- Preliminary Experimental Results
- Technology Stack
- Installation and Usage
- Project Structure
- Limitations
- Future Improvements
- Reproducibility and Responsible Use
- References
Overview
Digital content can be generated or modified using increasingly accessible AI tools. Images may be artificially generated, photographs may be manipulated, and document information may be altered or incorrectly represented.

VeriShield AI explores how different computational techniques can support digital content integrity analysis through a unified application.

The framework contains three modules:
1. AI-generated image detection: Classifies images into real and AI-generated categories.
2. Receipt verification: Extracts receipt information using OCR and checks field completeness and logical consistency through predefined rules.
3. Image tampering detection: Classifies images as authentic or manipulated and provides Grad-CAM visualizations to help interpret model predictions.
The modules address different integrity-related tasks. Their outputs are not interchangeable: an AI-generation classifier does not prove whether an image was edited, and a receipt consistency score does not establish whether a receipt was issued by a legitimate merchant.
Key Features
- Image classification for AI-generated content analysis.
- OCR-based receipt text extraction.
- Extraction of merchant, date, invoice number, subtotal, tax, total, currency, phone number, and address where detectable.
- Rule-based validation of receipt fields and arithmetic consistency.
- Image manipulation classification.
- Grad-CAM visualizations for investigating image-classification predictions.
- Evaluation using task-appropriate metrics.
- A modular architecture designed to support further research and development.
System Architecture
The application organizes the workflow into three analysis paths.
                  User Input
                      |
             VeriShield AI Interface
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
      Image Input  Receipt Image  Image Input
          |           |           |
          v           v           v
     AI-Generated   Image         Tampering
       Detection    Preprocessing  Detection
          |           |           |
          v           v           v
     Class Output   OCR and       Class Output
                    Field         and Grad-CAM
                    Extraction
                        |
                        v
                  Rule Validation
                        |
                        v
                 Integrity Report
Each module follows its own processing and evaluation pipeline. Model predictions, OCR confidence, and rule-based scores represent different types of evidence and should be interpreted separately.
Module 1: AI-Generated Image Detection
Objective
To investigate whether an input image is more consistent with the real-image or AI-generated-image category represented in the training data.
Methodology
1. Load the input image.
2. Apply the preprocessing and image transformations required by the selected model.
3. Perform inference using a trained image-classification model.
4. Return the predicted class and the model's output scores.
5. Evaluate performance on held-out data using classification metrics.
Dataset
The implementation uses the CIFAKE dataset, which contains real and AI-generated images.

The documented dataset audit includes 120,000 images: a 100,000-image training partition and a 20,000-image test partition. The training partition was further divided into 85,000 training images and 15,000 validation images.

These splits must remain separate during training, model selection, and final evaluation.
Models
The notebooks explore CNN-based classification and pretrained architectures, including:
- Convolutional Neural Network (CNN)
- Xception
- EfficientNet-B0
The final deployed model should be identified only after the model-comparison experiment is rerun and its results are reconciled with the saved configuration and checkpoint.
Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- ROC-AUC, where valid prediction scores are available
Important: Earlier notebook outputs reported approximately 94% accuracy for the CNN and 98% for Xception. Other project artifacts identify EfficientNet-B0 as the selected model. Because these records are inconsistent and the complete comparison did not finish successfully, these figures should be treated as preliminary notebook-reported results rather than a finalized model leaderboard.
Module 2: Receipt Verification
Objective
To extract information from receipt images and check whether the detected fields satisfy predefined completeness and consistency rules.
Methodology
The current implementation is primarily an OCR and rule-based validation pipeline, rather than a trained receipt-authenticity classifier.

The processing workflow includes:
1. Image preprocessing: Resize smaller images where needed, convert to grayscale, apply denoising and contrast enhancement, and sharpen the image.
2. Text recognition: Use EasyOCR to detect and extract text.
3. Field extraction: Apply pattern matching and keyword-based logic to identify relevant receipt fields.
4. Field validation: Check field presence and basic formatting or consistency.
5. Arithmetic checks: Compare subtotal, tax, and total when the required values are available.
6. Score calculation: Combine selected indicators into a heuristic integrity score.
Receipt Fields
The pipeline attempts to extract:
- Merchant name
- Date
- Invoice number
- Subtotal
- Tax
- Total amount
- Currency
- Phone number
- Address
Extraction quality depends on image clarity, receipt layout, OCR output, and the field-extraction rules.
Heuristic Score
The current scoring implementation uses the following weights:
Component	Weight
OCR confidence	30%
Metadata validation	35%
Field completeness	20%
Logical consistency	15%


These weights define a rule-based score. They do not represent a calibrated probability that a receipt is authentic, and they should not be interpreted as validated fraud-detection accuracy.
Datasets
The evaluation workflow uses:
- SROIE: Scanned receipt images and associated information extraction annotations.
- CORD: Receipt images with structured semantic annotations.
These datasets support OCR and information-extraction evaluation. They do not, by themselves, establish whether every receipt is genuine or fraudulent.
Evaluation Metrics
- OCR confidence
- Character Error Rate (CER)
- Word Error Rate (WER)
- Field-level exact-match accuracy
- Processing time
- Field completeness and logical-consistency indicators
The current evaluation requires further auditing of text normalization, OCR token ordering, annotation alignment, and field schemas. Reported error rates exceeding 1 and low extraction accuracy for some fields should not be presented as reliable final performance without this validation.
Module 3: Image Tampering Detection
Objective
To classify an image as authentic or manipulated based on patterns learned from labeled image data, and to provide visual explanations that help users inspect model predictions.
Methodology
1. Load and preprocess an input image.
2. Run inference using a trained image-classification model.
3. Produce the predicted class and output scores.
4. Generate a Grad-CAM heatmap to highlight image regions that influence the selected class prediction.
5. Evaluate classification performance against labeled test data.
Datasets
The implementation uses:
- CASIA v2: An image manipulation dataset used for training, validation, and test evaluation.
- IMD2020: An image manipulation dataset used for external evaluation.
The documented CASIA partition contains 8,829 training images, 1,892 validation images, and 1,893 test images. The documented IMD2020 external evaluation contains 2,424 images.

The dataset labels, image counts, preprocessing, and partitioning should be checked against the exact files used in the final experiments.
Models
- CNN
- Xception
- EfficientNet-B0
Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-score
- Matthews Correlation Coefficient (MCC)
- ROC-AUC
- Inference time
- Grad-CAM localization metrics, when a suitable ground-truth localization protocol is available
Explainability
Grad-CAM provides a heatmap indicating regions that influence a model's classification decision. It is a diagnostic visualization, not proof of manipulation and not a pixel-level segmentation mask.

The current localization evaluation reported a mean IoU of approximately 0.056 and a median IoU of 0. These results do not support strong claims about reliable tampering localization.
Datasets
Module	Dataset	Purpose
AI-generated image detection	CIFAKE	Real versus AI-generated image classification
Receipt verification	SROIE	OCR and receipt information extraction evaluation
Receipt verification	CORD	Structured receipt information extraction evaluation
Image tampering detection	CASIA v2	Image manipulation classification
Image tampering detection	IMD2020	External image manipulation evaluation


Dataset Usage Guidelines
- Obtain datasets from their official sources or authorized repositories.
- Follow each dataset's license and usage conditions.
- Keep training, validation, and test data separate.
- Check for duplicate and near-duplicate images across partitions.
- Document preprocessing, exclusions, class mappings, and dataset versions.
- Do not merge datasets with incompatible labels without a justified and documented protocol.
Dataset availability does not imply permission to redistribute the original data. This repository should contain code and documentation rather than restricted dataset files.
Evaluation Methodology
Evaluation should be conducted independently for each module.
Classification
For image-classification tasks, report accuracy, precision, recall, F1-score, confusion matrices, and ROC-AUC when appropriate.

For binary classification, document which class is treated as positive and how predicted probabilities or scores are oriented.
OCR and Receipt Extraction
Evaluate OCR text against the corresponding ground-truth transcription using documented text normalization. Report CER and WER together with field-level exact-match accuracy.

Define how missing fields, multiple candidate values, punctuation, currency symbols, and formatting differences are handled. Include the number of samples evaluated for each field.
External Evaluation
For IMD2020, evaluate using the documented external dataset without using its test labels to tune the model. Report external results separately from CASIA v2 test results.
Reproducibility
Record the model checkpoint, random seed, dataset split, preprocessing configuration, class mapping, software versions, and evaluation script used for each experiment.
Preliminary Experimental Results
The following observations summarize the current experimental artifacts. They are not a finalized, fully validated performance benchmark.
Module 1
The notebook reports approximately 94% accuracy for CNN and 98% for Xception on 20,000 test examples. However, other project files disagree about whether Xception or EfficientNet-B0 is the selected model. A clean rerun is required before publishing a final comparison.
Module 2
The receipt pipeline performs OCR, field extraction, and rule-based consistency checks. Current evaluation artifacts indicate that extraction performance varies substantially across fields and datasets. OCR evaluation and annotation alignment must be corrected before the reported aggregate error rates can be considered trustworthy.
Module 3
The CASIA v2 test results recorded in the current artifacts are:
Model	Accuracy	Precision	Recall	F1-score	ROC-AUC
CNN	70.05%	62.82%	64.37%	63.58%	0.7595
Xception	75.22%	67.77%	74.38%	70.92%	0.8036
EfficientNet-B0	83.47%	74.89%	89.21%	81.42%	0.9108


These are recorded CASIA v2 results and should be reproduced before being treated as final research claims.

The IMD2020 results contain inconsistencies between the reported classification metrics. They should not be used as evidence of reliable external generalization until the underlying predictions, labels, confusion matrix, positive-class definition, and metric calculations have been audited.
Technology Stack
The project artifacts use or reference the following technologies:
- Python: Main implementation language.
- PyTorch: Deep-learning model development and inference.
- CNN, Xception, EfficientNet-B0: Image-classification architectures.
- EasyOCR: Text recognition for receipt images.
- OpenCV: Image preprocessing and computer-vision operations.
- Grad-CAM: Visual explanation of classification predictions.
- scikit-learn: Classification metrics and evaluation utilities.
- Jupyter Notebook: Experimentation and model evaluation.
- Streamlit: Application interface, where configured in the repository.
The exact dependency versions should be taken from the tested project environment and maintained in requirements.txt.
Installation and Usage
Prerequisites
- Python version supported by the project's dependencies.
- Git.
- The packages listed in requirements.txt.
- Authorized access to any required datasets and trained model checkpoints.
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
Replace the placeholders with the actual repository URL and directory name.
2. Create a virtual environment
python -m venv .venv
Activate it on Windows:
.venv\Scripts\activate
On macOS or Linux:
source .venv/bin/activate
3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
Use the dependency versions tested with the project. PyTorch installation may require a platform-specific command depending on CPU or GPU support.
4. Configure model and dataset paths
Before running the application:
- Place or download the required model checkpoints using the documented procedure.
- Update configuration files to point to the correct checkpoint and dataset locations.
- Confirm that the configured model architecture matches the checkpoint.
- Verify that dataset paths and class mappings are correct.
Do not assume that model weights or datasets are included in the repository unless they are explicitly committed or linked.
5. Run the application
If the repository's Streamlit entry point is app.py, run:
streamlit run app.py
If the entry point has a different filename or location, use the actual path documented in the repository.
6. Run evaluations
Use the notebook or evaluation scripts included in the repository, following the documented dataset preparation and configuration steps. Save evaluation outputs and logs so that results can be independently checked.
Project Structure
The following is a recommended structure. Adjust it to match the files that actually exist in your repository.
VeriShield-AI/
├── README.md
├── requirements.txt
├── .gitignore
├── app.py
├── configs/
├── notebooks/
│   ├── Module_01_AI_Image_Detection.ipynb
│   ├── model2.ipynb
│   └── Model3.ipynb
├── src/
│   ├── image_detection/
│   ├── receipt_verification/
│   ├── tampering_detection/
│   └── common/
├── evaluation/
├── tests/
├── reports/
└── docs/
The listed directory structure is a target organization, not a claim that every directory or file is already present.
Limitations
VeriShield AI is a prototype, and several limitations remain.
1. Dataset generalization: Performance on one dataset may not transfer to images produced by newer generative models, different cameras, or unfamiliar image-editing methods.
2. Model-selection consistency: Module 1's recorded model selection must be reconciled with the notebook outputs and inference configuration.
3. Receipt extraction errors: OCR errors, unusual layouts, image quality, and inconsistent formatting can affect field extraction.
4. Heuristic scoring: The receipt integrity score uses predefined weights and is not a calibrated probability of fraud or authenticity.
5. External evaluation: Module 3's IMD2020 metrics require auditing before external-generalization claims can be made.
6. Explainability limitations: Grad-CAM visualizations highlight influential regions but do not prove that a specific region was manipulated.
7. Potential dataset leakage: Duplicate or near-duplicate samples may inflate results if they appear across different dataset partitions.
8. Authenticity cannot be guaranteed: Classification outputs and consistency checks are indicators for further review, not definitive verification.
Future Improvements
Planned research and engineering improvements include:
- Rerun and standardize model selection for AI-generated image detection.
- Audit external tampering-detection metrics and evaluation scripts.
- Improve OCR normalization, receipt field extraction, and annotation alignment.
- Add automated tests for preprocessing, model loading, and metric calculations.
- Perform duplicate and near-duplicate checks across dataset splits.
- Add more robust external evaluation on datasets not used for model selection.
- Improve explainability evaluation with clearly defined localization ground truth.
- Calibrate scores only when suitable labeled validation data and a defensible calibration protocol are available.
- Document experiment configurations, checkpoint versions, and reproducible evaluation commands.
- Improve error reporting, input validation, and user-facing explanations.
Reproducibility and Responsible Use
VeriShield AI is intended for research, experimentation, and decision support.
- Do not use the system's outputs as the sole basis for financial, legal, academic, or other high-impact decisions.
- Do not treat a high model score as proof that an image is genuine or that a receipt is fraudulent.
- Inspect original content and seek independent evidence when integrity matters.
- Respect dataset licenses, privacy requirements, and applicable laws.
- Report evaluation limitations and avoid presenting preliminary experiments as validated results.
References
The following foundational works and resources are relevant to the techniques and datasets used in this project. Verify the bibliographic details, versions, and dataset links before formal academic submission.
1. J. Fridrich, D. Soukal, and J. Lukáš, “Detection of Copy-Move Forgery in Digital Images,” Proceedings of Digital Forensic Research Workshop, 2003.
2. A. Rössler et al., “FaceForensics++: Learning to Detect Manipulated Facial Images,” Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2019.
3. R. R. Selvaraju et al., “Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization,” Proceedings of the IEEE International Conference on Computer Vision (ICCV), 2017.
4. F. Chollet, “Xception: Deep Learning with Depthwise Separable Convolutions,” Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2017.
5. M. Tan and Q. V. Le, “EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks,” Proceedings of the International Conference on Machine Learning (ICML), 2019.
6. A. Krizhevsky, I. Sutskever, and G. E. Hinton, “ImageNet Classification with Deep Convolutional Neural Networks,” Advances in Neural Information Processing Systems (NeurIPS), 2012.
7. A. Howard et al., “Searching for MobileNetV3,” Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2019.
8. A. Kuznetsova et al., “The Open Images Dataset V4: Unified Image Classification, Object Detection, and Visual Relationship Detection at Scale,” International Journal of Computer Vision, 2020.
9. H. Li et al., “ICDAR2019 Competition on Scanned Receipt OCR and Information Extraction (SROIE),” Proceedings of the International Conference on Document Analysis and Recognition (ICDAR), 2019.
10. S. Park et al., “CORD: A Consolidated Receipt Dataset for Post-OCR Parsing,” Workshop on Document Intelligence, 2019.
11. A. Paszke et al., “PyTorch: An Imperative Style, High-Performance Deep Learning Library,” Advances in Neural Information Processing Systems (NeurIPS), 2019.
12. G. Bradski, “The OpenCV Library,” Dr. Dobb's Journal of Software Tools, 2000.
13. F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.
14. CIFAKE dataset: Consult the original dataset publication and official dataset repository for the exact version used.
15. CASIA v2 dataset: Consult the dataset's original publication and authorized distribution source.
16. IMD2020 dataset: Consult the original publication and dataset documentation for the exact version used.
17. EasyOCR: Consult the official repository and documentation for the version used in the experiments.
Project Author
Shristi Chandra
B.Tech in Computer Science and Engineering – Artificial Intelligence (CSE-AI)
Indira Gandhi Delhi Technical University for Women (IGDTUW), Delhi, India
Project
VeriShield AI: An Integrated Framework for Digital Content Integrity Analysis

This academic research project combines AI-generated image detection, OCR-based receipt verification, and image tampering detection using deep learning, computer vision, and explainable AI.
Research Interests
- Artificial Intelligence and Machine Learning
- Computer Vision and Deep Learning
- Digital Image Forensics
- Document Intelligence and Optical Character Recognition (OCR)
- Explainable Artificial Intelligence (XAI)
