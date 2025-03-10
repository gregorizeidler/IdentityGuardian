from deepface import DeepFace
import cv2
import dlib

def detect_face_swaps_or_edits(image_path):
    try:
        analysis = DeepFace.analyze(img_path=image_path, actions=['emotion', 'age', 'gender'])
        if 'error' in analysis:
            return True  
    except:
        return True  
    return False

def detect_crop_or_edit(image_path):
    img = cv2.imread(image_path)
    detector = dlib.get_frontal_face_detector()
    faces = detector(img, 1)
    return len(faces) == 0
