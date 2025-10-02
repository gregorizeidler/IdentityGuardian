from flask import request, jsonify
import os

from .services.report_generation import generate_final_report
from .services.face_analysis import detect_face_swaps_or_edits, detect_crop_or_edit, check_liveness
from .services.image_quality import analyze_lighting_and_quality
from .services.face_comparison import compare_faces
from .services.document_analysis import analyze_document

def init_routes(app):
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'message': 'IdentityGuardian API',
            'version': '1.0',
            'endpoints': {
                '/verify': 'POST - Identity verification endpoint'
            }
        })

    @app.route('/verify', methods=['POST'])
    def verify():
        if 'photo' not in request.files or 'document' not in request.files or 'name' not in request.form or 'document_type' not in request.form:
            return jsonify({'error': 'Missing required parameters'}), 400

        photo = request.files['photo']
        document = request.files['document']
        user_name = request.form['name']
        document_type = request.form['document_type']

        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], "photo.jpg")
        document_path = os.path.join(app.config['UPLOAD_FOLDER'], "document.jpg")
        photo.save(photo_path)
        document.save(document_path)

        # Análise facial
        face_swap_detected = detect_face_swaps_or_edits(photo_path)
        crop_or_edit_detected = detect_crop_or_edit(photo_path)
        brightness, contrast = analyze_lighting_and_quality(photo_path)
        liveness_detected = check_liveness(photo_path)
        similarity_score = compare_faces(photo_path, document_path)
        
        # Análise do documento
        document_analysis = analyze_document(document_path)

        # Geração do relatório final
        report = generate_final_report(
            gpt_analysis=None,
            user_name=user_name,
            document_type=document_type,
            similarity_score=similarity_score,
            face_swap_detected=face_swap_detected,
            crop_or_edit_detected=crop_or_edit_detected,
            brightness=brightness,
            contrast=contrast,
            liveness_detected=liveness_detected,
            document_analysis=document_analysis
        )

        return jsonify({
            "report": report,
            "face_swap_detected": face_swap_detected,
            "crop_or_edit_detected": crop_or_edit_detected,
            "brightness": brightness,
            "contrast": contrast,
            "liveness_detected": liveness_detected,
            "similarity_score": similarity_score,
            "document_analysis": document_analysis
        })
