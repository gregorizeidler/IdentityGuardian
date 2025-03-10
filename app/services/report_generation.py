from openai import OpenAI

def generate_final_report(gpt_analysis, face_swap_detected, crop_or_edit_detected, brightness, contrast):
    client = OpenAI()
    prompt = f"""
    Análise de verificação de identidade:

    - Face swap detectado: {face_swap_detected}
    - Imagem cortada/editada detectada: {crop_or_edit_detected}
    - Brilho da imagem: {brightness}
    - Contraste da imagem: {contrast}

    Gere um relatório detalhado sobre essas detecções.
    """

    response = client.completions.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=700
    )
    
    return response.choices[0].text
