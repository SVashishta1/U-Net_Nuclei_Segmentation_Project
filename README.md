# U-Net Nuclei Segmentation Project

This repository implements a U-Net model for automating nucleus detection in biomedical images using the 2018 Data Science Bowl dataset from Kaggle. The project leverages Docker and Singularity containers to ensure portability and reproducibility.

---

## Table of Contents

- [Dataset Consideration](#dataset-consideration)
- [Project Overview](#project-overview)
- [Dataset Summary](#dataset-summary)
  - [Description](#description)
  - [Structure](#structure)
- [Project Flow](#project-flow)
- [Requirements](#requirements)
- [How to Reproduce](#how-to-reproduce)
- [License](#license)
- [Files Included](#files-included)
- [Notes](#notes)

---

## Dataset Consideration

The 2018 Data Science Bowl dataset from Kaggle is subject to Kaggle’s terms of use, which allow use for personal, non-commercial purposes and competition participation. **Your project’s license should not conflict with these terms** (e.g., it should not imply unrestricted commercial use of the dataset).

---

## Project Overview

This project uses a pre-trained U-Net model (saved as `unet_model.h5`) to segment nuclei in biomedical images. The inference pipeline is executed on a subset (the first 11 images) of the `stage1_test` dataset.

---

![Nuclei Segmentation Example](output/0114f484a16c152baa2d82fdd43740880a762c93f436c8988ac461c5c9dbe7d5_plot.png)

## Dataset Summary

### Description

- **Source:** 2018 Data Science Bowl, titled “Spot Nuclei. Speed Cures.”
- **Objective:** Accelerate biomedical research by automating nucleus detection—a critical step in analyzing cellular responses for drug discovery in diseases such as cancer, heart disease, and rare disorders.
- **Challenge:** The dataset includes images with nuclei under various conditions, posing a challenge for models to generalize across different microscopy techniques and cell types.

### Structure

- **Training Data:** Used to train the U-Net model (not included in this repository; see source below).
- **Test Data (stage1_test):**
  - Contains over 600 subfolders, each named with a unique ID (e.g., `fec226e45f49ab81ab71e0eaa1248ba09b56a328338dce93a43f4044eababed5`).
  - Each subfolder contains an `images` subfolder with one PNG file named after the parent ID (e.g., `fec226e45f49.../images/fec226e45f49....png`).
  - **Note:** This project processes only the first 11 images from the test dataset.

---

## Project Flow

1. **Model Training:**  
   - A U-Net model was trained on the 2018 Data Science Bowl training dataset (not included) and saved as `unet_model.h5`.

2. **Script Development:**  
   - The `infer_unet.py` script processes test images to generate segmented masks and visualization plots.

3. **Containerization:**  
   - A Docker image (`unet-inference`) was built with all necessary dependencies and the model.
   - The Docker image was converted to a Singularity SIF file (`unet-infer.sif`) for deployment on a Linux VM.

4. **Inference:**  
   - The first 11 images from `stage1_test` are processed on a VM, with outputs saved to a mounted directory.

5. **Output Retrieval:**  
   - The Singularity file and resulting outputs are copied back to a local machine for analysis.

---

## Requirements

- **Docker:** For building and testing the container on macOS or Linux.
- **Singularity:** For running the container on a Linux VM (not natively supported on macOS).
- **Python Dependencies (included in the container):**
  - tensorflow
  - numpy
  - opencv-python-headless
  - matplotlib

_For exact versions, refer to `requirements.txt`._

---

License

Important: The 2018 Data Science Bowl dataset is subject to Kaggle’s Terms of Use and is restricted to non-commercial and competition-related activities.

Files Included
	•	Dockerfile.infer: Docker configuration file.
	•	infer_unet.py: Python script for inference on stage1_test.
	•	unet_model.h5: Pre-trained U-Net model.
	•	unet-infer.sif: Singularity container image.
	•	requirements.txt: Python dependencies (for reference).

Notes
	•	Singularity on macOS: Not natively supported. Use a Linux VM or the provided Singularity image.
	•	Dataset Size: The stage1_test directory is large (over 600 subfolders); this project processes only the first 11 images (for testing) (trained on whole training dataset).
To process all images, modify infer_unet.py by removing the [:11] slicing.
	•	Path Adjustments: Update file paths (e.g., /Users/svashi/...) as needed for your local environment.

