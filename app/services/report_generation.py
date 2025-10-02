from openai import OpenAI

def generate_final_report(gpt_analysis, user_name, document_type, similarity_score, face_swap_detected, crop_or_edit_detected, brightness, contrast, liveness_detected, document_analysis=None):
    client = OpenAI()
    
    # Preparar informações da análise de documentos
    doc_info = ""
    if document_analysis and document_analysis.get("success"):
        fields = document_analysis.get("fields", {})
        validation = document_analysis.get("validation", {})
        quality = document_analysis.get("quality", {})
        
        doc_info = f"""
    
    Document Analysis:
    - Document is valid: {validation.get('is_valid', False)}
    - Confidence: {validation.get('confidence', 0)}%
    - Extracted CPF: {fields.get('cpf', 'Not found')}
    - Extracted RG: {fields.get('rg', 'Not found')}
    - Extracted Name: {fields.get('nome', 'Not found')}
    - Birth Date: {fields.get('data_nascimento', 'Not found')}
    - Document quality: {"Good" if quality.get('is_good_quality') else "Poor"}
    - Issues: {', '.join(validation.get('issues', [])) if validation.get('issues') else 'None'}
    - Warnings: {', '.join(validation.get('warnings', [])) if validation.get('warnings') else 'None'}
        """
    elif document_analysis and not document_analysis.get("success"):
        doc_info = f"\n    Document Analysis Error: {document_analysis.get('error', 'Unknown error')}"
    
    prompt = f"""
    Identity verification analysis:

    - User name: {user_name}
    - Document type: {document_type}
    - Facial similarity score: {similarity_score}
    - Face swap detected: {face_swap_detected}
    - Cropped/edited image detected: {crop_or_edit_detected}
    - Image brightness: {brightness}
    - Image contrast: {contrast}
    - Liveness detected: {liveness_detected}{doc_info}

    Provide a detailed report in Portuguese with insights and recommendations for improving identity verification accuracy.
    Include a final verdict: APPROVED or REJECTED based on all the factors above.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in identity verification and document analysis. Provide detailed, professional reports in Portuguese."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        # Se falhar, retornar um relatório básico sem GPT
        return generate_basic_report(user_name, document_type, similarity_score, face_swap_detected, crop_or_edit_detected, liveness_detected, document_analysis)

def generate_basic_report(user_name, document_type, similarity_score, face_swap_detected, crop_or_edit_detected, liveness_detected, document_analysis):
    """Gera um relatório básico sem usar GPT (fallback)"""
    
    # Determinar veredito
    issues = []
    warnings = []
    
    if face_swap_detected:
        issues.append("Face swap detectado")
    if crop_or_edit_detected:
        issues.append("Imagem editada ou cortada detectada")
    if not liveness_detected:
        issues.append("Falha na detecção de liveness")
    
    # Análise de similaridade
    if isinstance(similarity_score, str):
        warnings.append(f"Erro na comparação facial: {similarity_score}")
        similarity_ok = False
    else:
        similarity_ok = similarity_score > 0.7
        if not similarity_ok:
            issues.append(f"Similaridade facial baixa ({similarity_score:.2%})")
    
    # Análise do documento
    doc_valid = False
    if document_analysis and document_analysis.get("success"):
        validation = document_analysis.get("validation", {})
        doc_valid = validation.get("is_valid", False)
        if not doc_valid:
            issues.append("Documento inválido ou ilegível")
        for issue in validation.get("issues", []):
            issues.append(f"Documento: {issue}")
    
    # Veredito final
    verdict = "APROVADO" if len(issues) == 0 and similarity_ok and doc_valid else "REJEITADO"
    
    report = f"""
=== RELATÓRIO DE VERIFICAÇÃO DE IDENTIDADE ===

Nome do Usuário: {user_name}
Tipo de Documento: {document_type}
Data da Análise: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

--- ANÁLISE FACIAL ---
• Similaridade facial: {similarity_score if isinstance(similarity_score, str) else f"{similarity_score:.2%}"}
• Face swap detectado: {'SIM ⚠️' if face_swap_detected else 'NÃO ✓'}
• Imagem editada: {'SIM ⚠️' if crop_or_edit_detected else 'NÃO ✓'}
• Liveness detectado: {'SIM ✓' if liveness_detected else 'NÃO ⚠️'}

--- ANÁLISE DO DOCUMENTO ---
"""
    
    if document_analysis and document_analysis.get("success"):
        fields = document_analysis.get("fields", {})
        validation = document_analysis.get("validation", {})
        report += f"""• Documento válido: {'SIM ✓' if doc_valid else 'NÃO ⚠️'}
• Confiança: {validation.get('confidence', 0)}%
• CPF extraído: {fields.get('cpf', 'Não encontrado')}
• RG extraído: {fields.get('rg', 'Não encontrado')}
• Nome extraído: {fields.get('nome', 'Não encontrado')}
"""
    else:
        report += f"• Erro na análise: {document_analysis.get('error', 'Erro desconhecido')}\n"
    
    report += f"""
--- PROBLEMAS IDENTIFICADOS ---
{chr(10).join(f'• {issue}' for issue in issues) if issues else '• Nenhum problema identificado ✓'}

--- AVISOS ---
{chr(10).join(f'• {warning}' for warning in warnings) if warnings else '• Nenhum aviso'}

=== VEREDITO FINAL: {verdict} ===
"""
    
    return report

# Importar datetime para o relatório básico
from datetime import datetime
