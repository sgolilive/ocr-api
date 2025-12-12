# OCR Language Detection API

A lightweight OCR microservice built using FastAPI, Tesseract OCR, and Pillow.
This API automatically:

* Downloads the required trained data files (first run only)
* Detects language in the image
* Selects the correct Tesseract model
* Extracts text from an image URL
* Returns OCR result via a simple GET endpoint

Perfect for small apps, browser scripts, automation tools, and internal services.

### 🚀 Features

* 🔍 Auto-detect image language using langdetect
* 🧠 OCR extraction via Tesseract (tessdata_best)
* 🌐 Image download from URL
* ⚡ FastAPI high-performance API
* 🏗 Pre-download traineddata files once to speed up runtime
* 🧩 Easy deploy to Render / Railway / Fly.io

### 🌐 API Usage

#### 📌 GET /ocr?url=IMAGE_URL
Extracts text from a remotely hosted image.

Example Request
```
GET /ocr?url=https://example.com/sample-image.jpg
```
#### Example Response
```
{
  "image_url": "https://example.com/sample.jpg",
  "detected_language": "en",
  "tesseract_lang": "eng",
  "text": "Hello world from OCR!"
}
```

### 🧠 How Language Detection Works

* Download image
* Try OCR using eng+spa+fra+deu+por (fast fallback set)
* Run langdetect.detect() on extracted text
* Map detected language → correct Tesseract model (e.g., "en" → "eng")
* Run full OCR using the correct trained data model

### 📁 Project Structure
```
.
├── app.py             # FastAPI server
├── ocr.py             # OCR logic (all internal functions private except process_image)
├── tessdata/          # Auto-downloaded Tesseract traineddata files
├── requirements.txt   # Python dependencies
├── runtime.txt        # Optional (for Heroku / Railway)
└── README.md          # Documentation
```
### 🔧 Installation

#### 1. Clone the repo
* git clone https://github.com/yourusername/ocr-api.git
* cd ocr-api

#### 2. Create virtual environment
* python3 -m venv venv
* source venv/bin/activate

#### 3. Install dependencies
* pip install -r requirements.txt