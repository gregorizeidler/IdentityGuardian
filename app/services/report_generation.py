from openai import OpenAI

def generate_final_report(gpt_analysis, face_swap_detected, crop_or_edit_detected, brightness, contrast):
    client = OpenAI()
    prompt = f"""
    Identity verification analysis:

    - Face swap detected: {face_swap_detected}
    - Cropped/edited image detected: {crop_or_edit_detected}
    - Image brightness: {brightness}
    - Image contrast: {contrast}

    Generate a detailed report on these detections.
    """

    response = client.completions.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=700
    )
    
    return response.choices[0].text
