import cv2
import numpy as np

def analyze_lighting_and_quality(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    brightness = np.mean(img)
    contrast = np.std(img)
    return brightness, contrast
