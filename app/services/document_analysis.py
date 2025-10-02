import cv2
import numpy as np
import pytesseract
from PIL import Image
import re

def analyze_document(document_path):
    """
    Analisa um documento usando Tesseract OCR e validação de imagem.
    Extrai texto, identifica campos importantes e verifica qualidade.
    """
    try:
        # Carregar imagem
        img = cv2.imread(document_path)
        if img is None:
            return {
                "success": False,
                "error": "Não foi possível carregar a imagem"
            }
        
        # 1. Análise de qualidade da imagem
        quality_analysis = analyze_image_quality(img)
        
        # 2. Pré-processamento da imagem para melhorar OCR
        processed_img = preprocess_for_ocr(img)
        
        # 3. Extração de texto com Tesseract
        pil_img = Image.fromarray(processed_img)
        extracted_text = pytesseract.image_to_string(pil_img, lang='por')
        
        # 4. Análise e extração de campos importantes
        document_fields = extract_document_fields(extracted_text)
        
        # 5. Validação do documento
        validation = validate_document(extracted_text, document_fields, quality_analysis)
        
        return {
            "success": True,
            "extracted_text": extracted_text,
            "fields": document_fields,
            "quality": quality_analysis,
            "validation": validation,
            "is_valid_document": validation["is_valid"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Erro na análise do documento: {str(e)}"
        }

def analyze_image_quality(img):
    """Analisa a qualidade da imagem do documento"""
    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Verificar brilho
    brightness = np.mean(gray)
    
    # Verificar contraste
    contrast = np.std(gray)
    
    # Verificar se está borrada (usando Laplaciano)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    is_blurry = blur_score < 100
    
    # Verificar resolução
    height, width = img.shape[:2]
    resolution = width * height
    
    return {
        "brightness": float(brightness),
        "contrast": float(contrast),
        "blur_score": float(blur_score),
        "is_blurry": is_blurry,
        "resolution": resolution,
        "width": width,
        "height": height,
        "is_good_quality": not is_blurry and brightness > 50 and contrast > 20
    }

def preprocess_for_ocr(img):
    """Pré-processa a imagem para melhorar a precisão do OCR"""
    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplicar threshold adaptativo para melhorar contraste
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Remover ruído
    processed = cv2.medianBlur(processed, 3)
    
    return processed

def extract_document_fields(text):
    """Extrai campos importantes do texto do documento"""
    fields = {
        "nome": None,
        "cpf": None,
        "rg": None,
        "data_nascimento": None,
        "data_emissao": None,
        "orgao_expedidor": None
    }
    
    # Normalizar texto para facilitar busca
    text_upper = text.upper()
    
    # Buscar CPF (formato: XXX.XXX.XXX-XX ou XXXXXXXXXXX)
    cpf_pattern = r'\d{3}\.?\d{3}\.?\d{3}-?\d{2}'
    cpf_match = re.search(cpf_pattern, text)
    if cpf_match:
        fields["cpf"] = cpf_match.group()
    
    # Buscar RG (formato variado)
    rg_pattern = r'(?:RG|REGISTRO GERAL|IDENTIDADE)[:\s]*([0-9]{1,3}\.?[0-9]{3}\.?[0-9]{3}-?[0-9X])'
    rg_match = re.search(rg_pattern, text_upper)
    if rg_match:
        fields["rg"] = rg_match.group(1)
    
    # Buscar data de nascimento (formato: DD/MM/YYYY)
    birth_pattern = r'(?:NASCIMENTO|DATA NASC|NASC)[:\s]*(\d{2}[/-]\d{2}[/-]\d{4})'
    birth_match = re.search(birth_pattern, text_upper)
    if birth_match:
        fields["data_nascimento"] = birth_match.group(1)
    
    # Buscar data de emissão
    issue_pattern = r'(?:EMISSÃO|EMISSAO|DATA EMISSÃO)[:\s]*(\d{2}[/-]\d{2}[/-]\d{4})'
    issue_match = re.search(issue_pattern, text_upper)
    if issue_match:
        fields["data_emissao"] = issue_match.group(1)
    
    # Buscar órgão expedidor
    org_pattern = r'(?:SSP|DETRAN|PC|IFP|PM|CGPI)[/-]?([A-Z]{2})'
    org_match = re.search(org_pattern, text_upper)
    if org_match:
        fields["orgao_expedidor"] = org_match.group()
    
    # Tentar extrair nome (geralmente após "NOME" ou nas primeiras linhas)
    name_pattern = r'(?:NOME|NAME)[:\s]*([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+)'
    name_match = re.search(name_pattern, text_upper)
    if name_match:
        fields["nome"] = name_match.group(1).strip()
    
    return fields

def validate_document(text, fields, quality):
    """Valida se o documento parece ser autêntico e legível"""
    validation = {
        "is_valid": False,
        "confidence": 0,
        "issues": [],
        "warnings": []
    }
    
    score = 0
    max_score = 100
    
    # Verificar qualidade da imagem (30 pontos)
    if quality["is_good_quality"]:
        score += 30
    else:
        validation["issues"].append("Qualidade da imagem ruim")
        if quality["is_blurry"]:
            validation["issues"].append("Imagem borrada")
        if quality["brightness"] < 50:
            validation["issues"].append("Imagem muito escura")
        if quality["contrast"] < 20:
            validation["issues"].append("Contraste insuficiente")
    
    # Verificar se tem texto extraído (20 pontos)
    if text and len(text.strip()) > 50:
        score += 20
    else:
        validation["issues"].append("Pouco ou nenhum texto extraído")
    
    # Verificar campos importantes (50 pontos)
    if fields["cpf"]:
        score += 15
    else:
        validation["warnings"].append("CPF não encontrado")
    
    if fields["rg"]:
        score += 15
    else:
        validation["warnings"].append("RG não encontrado")
    
    if fields["nome"]:
        score += 10
    else:
        validation["warnings"].append("Nome não encontrado")
    
    if fields["data_nascimento"]:
        score += 10
    else:
        validation["warnings"].append("Data de nascimento não encontrada")
    
    # Verificar se contém palavras-chave de documentos brasileiros
    keywords = ["REPUBLICA FEDERATIVA", "BRASIL", "IDENTIDADE", "REGISTRO", "CPF"]
    text_upper = text.upper()
    keyword_count = sum(1 for keyword in keywords if keyword in text_upper)
    
    if keyword_count >= 2:
        score += 10
    else:
        validation["warnings"].append("Documento não parece ser brasileiro")
    
    validation["confidence"] = min(score, max_score)
    validation["is_valid"] = score >= 50  # Mínimo de 50% para considerar válido
    
    return validation
