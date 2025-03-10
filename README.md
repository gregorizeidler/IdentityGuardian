# IdentityGuardian - Identity Verification System

## 📌 About the Project
**IdentityGuardian** is a Flask API designed for **identity verification** using Artificial Intelligence. The system detects image fraud, identifies facial manipulations, assesses image quality, and verifies document authenticity.

## 🚀 Features
- 🔍 **Identity verification** with facial analysis
- 🤖 **Photo manipulation detection** (deepfake, face swap, cropping)
- 🧑‍🏫 **Age and gender estimation** from images
- 💡 **Image quality analysis** (brightness, contrast)
- 📄 **Comparison of documents and selfies**
- 📊 **Detailed report generation** using OpenAI GPT-4

## 🏗️ Project Structure

```
IdentityGuardian/
│── app/
│   ├── __init__.py            # Initializes Flask app
│   ├── routes.py              # Defines API routes
│   ├── services/              # Service modules
│   │   ├── face_analysis.py   # Facial analysis using DeepFace
│   │   ├── document_analysis.py # Placeholder for document analysis
│   │   ├── image_quality.py   # Brightness and contrast analysis
│   │   ├── report_generation.py # Report generation with OpenAI GPT
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

### Expected Response:
```json
{
    "face_swap_detected": false,
    "crop_or_edit_detected": true,
    "brightness": 150.4,
    "contrast": 52.3
}
```

## 🛠️ Technologies Used
- **Flask** - API Framework
- **OpenCV** - Image Processing
- **DeepFace** - Facial Analysis
- **OpenAI GPT-4** - Report Generation
- **Dlib** - Facial Detection
- **Facenet-PyTorch** - Feature Extraction

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Contributing
Feel free to open issues and submit pull requests! All contributions are welcome. 🚀
