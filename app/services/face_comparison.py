from deepface import DeepFace

def compare_faces(photo_path, document_path):
    try:
        result = DeepFace.verify(photo_path, document_path)
        return result['similarity'] if 'similarity' in result else result['distance']
    except Exception as e:
        return str(e)
