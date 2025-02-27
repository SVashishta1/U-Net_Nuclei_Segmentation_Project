import tensorflow as tf
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import glob

# Defining the paths
MODEL_PATH = "/app/unet_model.h5"
INPUT_DIR = "/app/stage1_test"  
OUTPUT_DIR = "/app/output"


os.makedirs(OUTPUT_DIR, exist_ok=True) # an folder for the output results

# Loading the trained model 
print(f" Loading model from: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)

# Loading and preprocessing the images
def preprocess_image(image_path, img_size=(256, 256)):
    print(f" Processing image: {image_path}")
    if not os.path.exists(image_path):
        print(f" Error: Image not found at {image_path}")
        return None
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f" Error: Failed to load image at {image_path}")
        return None
    img = cv2.resize(img, img_size)
    img = img / 255.0  # Normalizing
    return img.reshape(1, img_size[0], img_size[1], 3)

# Processing all images in the input directory
image_paths = glob.glob(os.path.join(INPUT_DIR, "*/images/*.png"))  # getting all PNG images from the sub folders
successful_count = 0

for image_path in image_paths[:11]:  # Testing with only first 11 images
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]  
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}_segmented.png")
    plot_path = os.path.join(OUTPUT_DIR, f"{base_name}_plot.png")

    # Preprocess the image
    image = preprocess_image(image_path)
    if image is None:
        continue  # Skip to next image if preprocessing fails

    # Predection phase
    pred_mask = model.predict(image)[0]

    # Converting prediction to binary mask
    binary_mask = (pred_mask > 0.5).astype(np.uint8) * 255

    # Save the segmented output
    try:
        success = cv2.imwrite(output_path, binary_mask)
        if success:
            print(f" Segmentation complete! Saved to {output_path}")
            successful_count += 1
        else:
            print(f" Failed to save segmented output to {output_path}")
    except Exception as e:
        print(f" Error saving segmented output: {e}")

    # Save the results as an image
    try:
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.imread(image_path))
        plt.title("Original Image")
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.imshow(binary_mask, cmap="gray")
        plt.title("Predicted Segmentation Mask")
        plt.axis("off")

        plt.savefig(plot_path, bbox_inches="tight")
        print(f" Plot saved to {plot_path}")
        plt.close()  # Close the figure to free memory
    except Exception as e:
        print(f" Error saving plot: {e}")

print(f" Processed {successful_count} of {min(11, len(image_paths))} images successfully!")
