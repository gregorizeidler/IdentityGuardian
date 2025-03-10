from openai import OpenAI

def generate_final_report(gpt_analysis, user_name, document_type, similarity_score, face_swap_detected, crop_or_edit_detected, brightness, contrast, liveness_detected):
    client = OpenAI()
    prompt = f"""
    Identity verification analysis:

    - User name: {user_name}
    - Document type: {document_type}
    - Facial similarity score: {similarity_score}
    - Face swap detected: {face_swap_detected}
    - Cropped/edited image detected: {crop_or_edit_detected}
    - Image brightness: {brightness}
    - Image contrast: {contrast}
    - Liveness detected: {liveness_detected}

    Provide a detailed report with insights and recommendations for improving identity verification accuracy.
    """

    response = client.completions.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=700
    )
    
    return response.choices[0].text
