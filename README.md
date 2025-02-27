
Dataset Consideration: The 2018 Data Science Bowl dataset from Kaggle is subject to Kaggle’s terms of use, which allow use for personal, non-commercial purposes and competition participation. Your project’s license should not conflict with this (e.g., not imply unrestricted commercial use of the dataset).

U-Net Nuclei Segmentation Project
This project implements a U-Net model to automate nucleus detection in biomedical images, leveraging the 2018 Data Science Bowl dataset. The solution uses Docker and Singularity containers for portability and reproducibility, targeting the first 11 images from the stage1_test dataset.
Dataset Summary
Description
The dataset comes from the 2018 Data Science Bowl, titled "Spot Nuclei. Speed Cures.". The challenge aims to accelerate biomedical research by automating nucleus detection in cell images. Identifying nuclei is a critical first step in analyzing cellular responses to treatments, enabling faster drug discovery for diseases like cancer, heart disease, and rare disorders. The dataset includes a diverse set of images with nuclei under varied conditions, challenging models to generalize across different microscopy techniques and cell types.
Structure
Training Data: Used to train the U-Net model (not included in this repo; see source below).
Test Data (stage1_test):
Contains over 600 subfolders, each named with a unique ID (e.g., fec226e45f49ab81ab71e0eaa1248ba09b56a328338dce93a43f4044eababed5).
Each subfolder has an images subfolder with one PNG file named after the parent ID (e.g., fec226e45f49.../images/fec226e45f49....png).
This project processes the first 11 images from this set.
Source
Kaggle: 2018 Data Science Bowl
Overview Videos:
Snapshot
Why Nuclei?
Project Flow
Model Training: A U-Net model was trained on the 2018 Data Science Bowl training dataset (not included here) to detect nuclei, saved as unet_model.h5.
Script Development: infer_unet.py processes test images, generating segmented masks and visualization plots.
Containerization:
Built a Docker image (unet-inference) with dependencies and the model.
Converted it to a Singularity SIF file (unet-infer.sif) for deployment on a Linux VM.
Inference: Processed the first 11 images from stage1_test on a VM, saving outputs to a mounted directory.
Output Retrieval: Copied the SIF file and results back to the Mac for analysis.
Requirements
Docker: For building and testing the container on macOS or Linux.
Singularity: For running the container on a Linux VM (not natively supported on macOS).
Python Dependencies (included in the container):
tensorflow
numpy
opencv-python-headless
matplotlib
See requirements.txt for exact versions used.

How to Reproduce
This section guides you through reproducing the project, assuming all files (Dockerfile.infer, infer_unet.py, unet_model.h5, unet-infer.sif, etc.) are in the GitHub repository root. You’ll need the stage1_test dataset from Kaggle.
1. Clone the Repository
bash

git clone https://github.com/SVashishta1/U-Net_Nuclei_Segmentation_Project.git
cd U-Net_Nuclei_Segmentation_Project
3. Obtain the Dataset
Download the 2018 Data Science Bowl dataset from Kaggle.
Extract stage1_test.zip into the repository directory:
bash
unzip stage1_test.zip -d .
Resulting structure: ./stage1_test/<id>/images/<id>.png.
4. Build the Docker Image (Optional, if Modifying)
If you want to rebuild the Docker image from scratch (e.g., to update infer_unet.py):
bash
docker build --no-cache -t unet-inference -f Dockerfile.infer .
Note: Skip this if using the provided unet-infer.sif.
5. Test Locally with Docker (macOS/Linux)
Run the container with stage1_test and an output directory:
bash
mkdir -p output
docker run --rm -v $(pwd)/stage1_test:/app/stage1_test -v $(pwd)/output:/app/output unet-inference
Check outputs:
bash
ls -l output/
Interactive Debugging (optional):
bash
docker run -it -v $(pwd)/stage1_test:/app/stage1_test -v $(pwd)/output:/app/output unet-inference bash
# Inside container:
ls -l /app/stage1_test/*/images/  # Verify images
python3 -u infer_unet.py          # Run script
ls -l /app/output                 # Check outputs
exit
5. Convert Docker Image to Singularity SIF (If Needed)
On a Linux Machine (not macOS, unless using a VM):
Save the Docker image:
bash
docker save -o unet-inference.tar unet-inference
Build SIF:
bash
singularity build unet-infer.sif docker-archive://unet-inference.tar
Note: Use the provided unet-infer.sif in the repo to skip this step.
6. Run on a Linux VM with Singularity
Transfer Files to VM:
bash
scp unet-infer.sif stage1_test vboxuser@<vm-ip>:/home/vboxuser/apptainer/
Replace <vm-ip> with your VM’s IP address.
SSH into VM:
bash
ssh vboxuser@<vm-ip>
Run the Container:
bash
mkdir -p /home/vboxuser/apptainer/output
singularity run --bind /home/vboxuser/apptainer/stage1_test:/app/stage1_test,/home/vboxuser/apptainer/output:/app/output unet-infer.sif
Check Outputs:
bash
ls -l /home/vboxuser/apptainer/output/
7. Retrieve Results to Your Machine
From your Mac:
bash
scp -P 2222 vboxuser@localhost:/home/vboxuser/apptainer/output/* /Users/svashi/Documents/Vashishta/Projects/med_Project/project_files/cell_pipeline/final_deliverables/
Adjust -P 2222 if your VM uses a different SSH port (default is 22 for remote VMs).
For a remote VM, use <vm-ip> instead of localhost.
License
This project is licensed under the MIT License—see the LICENSE file for details. Note that the 2018 Data Science Bowl dataset (not included) is subject to Kaggle’s Terms of Use, which restrict its use to non-commercial purposes and competition-related activities.
Files Included
Dockerfile.infer: Docker configuration file.
infer_unet.py: Python script for inference on stage1_test.
unet_model.h5: Pre-trained U-Net model.
unet-infer.sif: Singularity container image.
requirements.txt: Python dependencies (for reference).
Notes
Singularity on macOS: Not natively supported; use a Linux VM or the pre-built unet-infer.sif.
Dataset Size: stage1_test is large (>600 subfolders); this project processes only the first 11 images. Modify infer_unet.py (remove [:11]) to process all.
Commands: Adjust paths (e.g., /Users/svashi/...) to your local setup.

