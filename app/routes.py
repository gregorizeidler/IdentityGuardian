from flask import request, jsonify
from .services.face_analysis import detect_face_swaps_or_edits, detect_crop_or_edit
from .services.image_quality import analyze_lighting_and_quality
import os

def init_routes(app):
    
    @app.route('/verify', methods=['POST'])
    def verify():
        if 'photo' not in request.files or 'document' not in request.files:
            return jsonify({'error': 'Envie uma foto e um documento'}), 400

        photo = request.files['photo']
        document = request.files['document']
        
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], "photo.jpg")
        document_path = os.path.join(app.config['UPLOAD_FOLDER'], "document.jpg")
        photo.save(photo_path)
        document.save(document_path)

        face_swap_detected = detect_face_swaps_or_edits(photo_path)
        crop_or_edit_detected = detect_crop_or_edit(photo_path)
        brightness, contrast = analyze_lighting_and_quality(photo_path)

        return jsonify({
            "face_swap_detected": face_swap_detected,
            "crop_or_edit_detected": crop_or_edit_detected,
            "brightness": brightness,
            "contrast": contrast
        })
