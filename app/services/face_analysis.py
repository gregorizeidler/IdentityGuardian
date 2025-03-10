import cv2
import numpy as np
from deepface import DeepFace
import dlib

def detect_face_swaps_or_edits(image_path):
    try:
        analysis = DeepFace.analyze(img_path=image_path, actions=['emotion', 'age', 'gender'])
        if 'error' in analysis:
            return True  # If detection fails, it may be an edited image
    except:
        return True  # If analysis fails, manipulation is suspected
    return False

def detect_crop_or_edit(image_path):
    img = cv2.imread(image_path)
    detector = dlib.get_frontal_face_detector()
    faces = detector(img, 1)
    return len(faces) == 0

def check_liveness(image_path):
    """
    Detects if the image is a real selfie or a photo of a photo.
    """
    img = cv2.imread(image_path)
    edges = cv2.Canny(img, 100, 200)
    edge_density = np.sum(edges) / (img.shape[0] * img.shape[1])
    return edge_density < 0.02  # Adjust threshold based on testing
