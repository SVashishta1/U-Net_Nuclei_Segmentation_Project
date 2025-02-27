import numpy as np
import pandas as pd
import os
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Concatenate
from tensorflow.keras.models import Model

# GPU CHECK: Enable GPU if available
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(" GPU Detected! Enabling GPU acceleration for TensorFlow.")
    tf.config.experimental.set_memory_growth(gpus[0], True)
else:
    print(" No GPU found. Using CPU for training. Training may be slow.")

# Setting dataset path
DATASET_PATH = "/Users/svashi/Documents/Vashishta/Projects/UPenn_Prep_Project/project_files/cell_pipeline/datasets/cell_segmantation/stage1_train"  # Update this

print(" Dataset Path:", DATASET_PATH)

# loading images & masks
def load_image_and_mask(image_id, img_size=(256, 256)):
    if image_id.startswith("."):  # to ignore system files like .DS_Store
        return None, None

    image_path = f"{DATASET_PATH}/{image_id}/images/{image_id}.png"
    
    if not os.path.exists(image_path):
        print(f" Warning: Image not found: {image_path}")
        return None, None

    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    if image is None:
        print(f" Warning: Failed to load image: {image_path}")
        return None, None

    image = cv2.resize(image, img_size)

    mask_folder = f"{DATASET_PATH}/{image_id}/masks/"
    
    mask = np.zeros((img_size[0], img_size[1]), dtype=np.uint8)
    mask_count = 0

    for mask_file in os.listdir(mask_folder):
        if mask_file.startswith("."):
            continue
        mask_path = os.path.join(mask_folder, mask_file)
        mask_img = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if mask_img is None:
            print(f" Warning: Failed to load mask: {mask_path}")
            continue

        mask_img = cv2.resize(mask_img, img_size)
        mask = np.maximum(mask, mask_img)
        mask_count += 1

    mask = (mask > 0).astype(np.uint8) * 255
    print(f" Processed {image_id} | Masks Combined: {mask_count}")
    return image, mask

# Preparing dataset
x_train, y_train = [], []
image_count = 0

print("\n Loading dataset...")

for image_id in os.listdir(DATASET_PATH):
    img, mask = load_image_and_mask(image_id)
    if img is None or mask is None:
        continue
    x_train.append(img)
    y_train.append(mask)
    image_count += 1
    if image_count % 50 == 0:
        print(f" Processed {image_count} images...")

print(f"\n Dataset Loaded | Total Images Processed: {image_count}")
x_train = np.array(x_train) / 255.0
y_train = np.array(y_train) / 255.0

# Defining U-Net model
def unet_model(input_size=(256, 256, 3)):
    inputs = Input(input_size)
    conv1 = Conv2D(64, 3, activation='relu', padding='same')(inputs)
    conv1 = Conv2D(64, 3, activation='relu', padding='same')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(128, 3, activation='relu', padding='same')(pool1)
    conv2 = Conv2D(128, 3, activation='relu', padding='same')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(256, 3, activation='relu', padding='same')(pool2)
    conv3 = Conv2D(256, 3, activation='relu', padding='same')(conv3)

    up4 = UpSampling2D(size=(2,2))(conv3)
    up4 = Concatenate()([conv2, up4])
    conv4 = Conv2D(128, 3, activation='relu', padding='same')(up4)
    conv4 = Conv2D(128, 3, activation='relu', padding='same')(conv4)

    up5 = UpSampling2D(size=(2,2))(conv4)
    up5 = Concatenate()([conv1, up5])
    conv5 = Conv2D(64, 3, activation='relu', padding='same')(up5)
    conv5 = Conv2D(64, 3, activation='relu', padding='same')(conv5)

    outputs = Conv2D(1, 1, activation='sigmoid')(conv5)

    model = Model(inputs, outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

print("\n Initializing U-Net Model...")
model = unet_model()
model.summary()

print("\n Starting Training...\n")

history = model.fit(
    x_train, y_train, 
    batch_size=8, 
    epochs=10, 
    validation_split=0.2,
    verbose=1
)

print("\n Training Complete!")

# Saving the trained model
model.save("unet_model.h5")
print("\n Model saved as unet_model.h5 ")