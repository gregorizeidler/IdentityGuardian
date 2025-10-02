# IdentityGuardian - Identity Verification System

## 📌 About the Project
**IdentityGuardian** is a Flask API designed for **identity verification** using Artificial Intelligence. The system detects image fraud, identifies facial manipulations, assesses image quality, and verifies document authenticity.

## 🚀 Features
- 🔍 **Identity verification** with facial analysis and similarity score
- 🛡️ **Liveness detection** (ensures the selfie is real)
- 🤖 **Photo manipulation detection** (deepfake, face swap, cropping)
- 🧑‍🏫 **Age and gender estimation** from images
- 💡 **Image quality analysis** (brightness, contrast)
- 📄 **Comparison of documents and selfies**
- 📝 **Document OCR analysis** (extracts CPF, RG, name, dates)
- 📊 **Detailed report generation** using OpenAI GPT-4

## 🏗️ Project Structure

```
IdentityGuardian/
│── app/
│   ├── __init__.py            # Initializes Flask app
│   ├── routes.py              # Defines API routes
│   ├── services/              # Service modules
│   │   ├── face_analysis.py   # Facial analysis using DeepFace
│   │   ├── document_analysis.py # Document OCR analysis with Tesseract
│   │   ├── image_quality.py   # Brightness and contrast analysis
│   │   ├── report_generation.py # Report generation with OpenAI GPT
│   │   ├── face_comparison.py  # Face similarity detection
│── uploads/                   # Folder for temporary file storage
│── run.py                     # Main file to run the API
│── requirements.txt            # Project dependencies
│── README.md                   # Project documentation
│── .gitignore                  # Files to be ignored in Git
```

## 🔧 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/IdentityGuardian.git
   cd IdentityGuardian
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the API:
   ```bash
   python run.py
   ```

4. Access the API via browser or Postman:
   ```
   http://127.0.0.1:5000/
   ```

## 🎯 How to Use
The API provides the `/verify` endpoint, where you can upload images for analysis.

### Request Example
**POST** `/verify`

#### Expected Parameters:
- `photo`: Selfie image (file)
- `document`: Document image (file)
- `name`: User's name (string)
- `document_type`: Type of document (`RG`, `CNH`, `Passport`)
- `birth_date`: Date of birth (`DD/MM/YYYY`)

#### Example cURL Command:
```bash
curl -X POST "http://127.0.0.1:5000/verify" \
    -F "photo=@selfie.jpg" \
    -F "document=@document.jpg" \
    -F "name=John Doe" \
    -F "document_type=RG" \
    -F "birth_date=08/15/1990"
```

### Expected Response (Caso APROVADO):
```json
{
    "report": "=== RELATÓRIO DE VERIFICAÇÃO DE IDENTIDADE === | Nome do Usuário: John Doe | Tipo de Documento: RG | Data da Análise: 02/10/2025 14:30:15 | --- ANÁLISE FACIAL --- | • Similaridade facial: 98.3% | • Face swap detectado: NÃO ✓ | • Imagem editada: NÃO ✓ | • Liveness detectado: SIM ✓ | --- ANÁLISE DO DOCUMENTO --- | • Documento válido: SIM ✓ | • Confiança: 85% | • CPF extraído: 123.456.789-00 | • RG extraído: 12.345.678-9 | • Nome extraído: JOHN DOE | --- PROBLEMAS IDENTIFICADOS --- | • Nenhum problema identificado ✓ | === VEREDITO FINAL: APROVADO ===",
    "face_swap_detected": false,
    "crop_or_edit_detected": false,
    "brightness": 150.4,
    "contrast": 52.3,
    "liveness_detected": true,
    "similarity_score": 0.983,
    "document_analysis": {
        "success": true,
        "extracted_text": "REPÚBLICA FEDERATIVA DO BRASIL | MINISTÉRIO DA JUSTIÇA | SECRETARIA DE SEGURANÇA PÚBLICA | REGISTRO DE IDENTIDADE CIVIL | NOME: JOHN DOE | RG: 12.345.678-9 | CPF: 123.456.789-00 | NASCIMENTO: 15/08/1990 | FILIAÇÃO: MARIA DOE E JOSE DOE | NATURALIDADE: SÃO PAULO - SP | DATA EMISSÃO: 10/01/2015 | ÓRGÃO EXPEDIDOR: SSP-SP",
        "fields": {
            "nome": "JOHN DOE",
            "cpf": "123.456.789-00",
            "rg": "12.345.678-9",
            "data_nascimento": "15/08/1990",
            "data_emissao": "10/01/2015",
            "orgao_expedidor": "SSP-SP"
        },
        "quality": {
            "brightness": 145.7,
            "contrast": 48.9,
            "blur_score": 325.8,
            "is_blurry": false,
            "resolution": 2073600,
            "width": 1920,
            "height": 1080,
            "is_good_quality": true
        },
        "validation": {
            "is_valid": true,
            "confidence": 85,
            "issues": [],
            "warnings": []
        },
        "is_valid_document": true
    }
}
```

### Expected Response (Caso REJEITADO):
```json
{
    "report": "=== RELATÓRIO DE VERIFICAÇÃO DE IDENTIDADE === | Nome do Usuário: Maria Silva | Tipo de Documento: RG | Data da Análise: 02/10/2025 15:45:30 | --- ANÁLISE FACIAL --- | • Similaridade facial: 45% | • Face swap detectado: SIM ⚠️ | • Imagem editada: SIM ⚠️ | • Liveness detectado: NÃO ⚠️ | --- ANÁLISE DO DOCUMENTO --- | • Documento válido: NÃO ⚠️ | • Confiança: 35% | • CPF extraído: Não encontrado | • RG extraído: 98.765.432-1 | • Nome extraído: MARIA SILVA | --- PROBLEMAS IDENTIFICADOS --- | • Face swap detectado | • Imagem editada ou cortada detectada | • Falha na detecção de liveness | • Similaridade facial baixa (45.00%) | • Documento inválido ou ilegível | • Documento: Qualidade da imagem ruim | • Documento: Imagem borrada | • Documento: Imagem muito escura | === VEREDITO FINAL: REJEITADO ===",
    "face_swap_detected": true,
    "crop_or_edit_detected": true,
    "brightness": 35.2,
    "contrast": 15.8,
    "liveness_detected": false,
    "similarity_score": 0.45,
    "document_analysis": {
        "success": true,
        "extracted_text": "IDENTIDADE | RG 98765432-1 | MARIA SILVA | NASCIMENTO 20/03/1985",
        "fields": {
            "nome": "MARIA SILVA",
            "cpf": null,
            "rg": "98.765.432-1",
            "data_nascimento": "20/03/1985",
            "data_emissao": null,
            "orgao_expedidor": null
        },
        "quality": {
            "brightness": 42.3,
            "contrast": 18.5,
            "blur_score": 65.4,
            "is_blurry": true,
            "resolution": 921600,
            "width": 1280,
            "height": 720,
            "is_good_quality": false
        },
        "validation": {
            "is_valid": false,
            "confidence": 35,
            "issues": [
                "Qualidade da imagem ruim",
                "Imagem borrada",
                "Imagem muito escura"
            ],
            "warnings": [
                "CPF não encontrado",
                "Data de emissão não encontrada",
                "Órgão expedidor não encontrado",
                "Documento não parece ser brasileiro"
            ]
        },
        "is_valid_document": false
    }
}
```

## 🛠️ Technologies Used
- **Flask** - API Framework
- **OpenCV** - Image Processing
- **DeepFace** - Facial Analysis
- **Tesseract OCR** - Document text extraction
- **Pillow** - Image manipulation
- **OpenAI GPT-4** - Report Generation
- **Dlib** - Facial Detection
- **TensorFlow** - Deep Learning backend

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Contributing
Feel free to open issues and submit pull requests! All contributions are welcome. 🚀
