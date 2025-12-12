# 🏥 Reportify - Medical Report Generator

A professional medical report generator that converts JSON patient data to beautifully formatted PDF reports.

## 🌟 Features

- **FastAPI REST API** - Modern, fast API for JSON to PDF conversion
- **Flask Web Interface** - Traditional web app for patient dashboard
- **MongoDB Integration** - Store and retrieve patient health data
- **AI-Powered Insights** - Gemini AI for medical test summaries and recommendations
- **Professional PDF Reports** - High-quality medical reports with custom fonts and branding
- **Barcode Generation** - Unique barcodes for each report

## 📁 Project Structure

```
reportify/
├── app/
│   ├── api/                    # FastAPI endpoints
│   │   └── v1/
│   │       ├── endpoints/      # API route handlers
│   │       └── router.py       # API router configuration
│   ├── core/                   # Core functionality
│   │   ├── config.py          # Application settings
│   │   └── database.py        # Database connections
│   ├── models/                 # Pydantic data models
│   │   └── report.py          # Report schemas
│   ├── services/               # Business logic
│   │   ├── data_fetching.py   # Data retrieval & AI
│   │   └── pdf_generator.py   # PDF generation service
│   ├── utils/                  # Utilities
│   │   └── pdf_pages.py       # PDF page builders
│   └── web/                    # Flask web routes
│       └── routes.py          # Web UI routes
├── static/                     # Static assets (CSS, JS, images)
├── templates/                  # HTML templates
├── resources/                  # Fonts and resources
│   └── fonts/                 # Custom fonts for PDFs
├── outputs/                    # Generated files
│   └── generated_pdfs/        # Output PDF reports
├── tests/                      # Test suite
├── main.py                     # FastAPI application entry
├── wsgi.py                     # Flask application entry
├── requirements.txt            # Python dependencies
└── .env.example               # Environment variables template
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- MongoDB
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AnandRajaM/reportify.git
cd reportify
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Set up MongoDB**
- Ensure MongoDB is running
- Update `MONGODB_URL` in `.env`

## 🎯 Usage

### Running FastAPI (Recommended for APIs)

```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

Access API documentation: `http://localhost:8000/api/docs`

### Running Flask (Web UI)

```bash
# Development
python wsgi.py

# Production with Gunicorn
gunicorn wsgi:app -w 4 -b 0.0.0.0:5000
```

Access web interface: `http://localhost:5000`

## 📡 API Endpoints

### Health Check
```http
GET /api/v1/reports/health
```

### Generate Report from Database
```http
POST /api/v1/reports/generate-report
Content-Type: application/json

{
  "customer_name": "John Doe",
  "booking_date": "2023-11-01 00:00:00 UTC",
  "include_highlights": true
}
```

### Convert JSON to PDF
```http
POST /api/v1/reports/json-to-pdf
Content-Type: application/json

{
  "patient_data": {
    "customer_name": "Jane Smith",
    "booking_date": "2023-12-01",
    "booking_id": "BK123456",
    "tests": [...]
  },
  "template_type": "standard",
  "include_barcode": true
}
```

### Download Report
```http
GET /api/v1/reports/download/{filename}
```

### List All Reports
```http
GET /api/v1/reports/list
```

## 🔧 Configuration

Edit `.env` file:

```env
# Database
MONGODB_URL=mongodb://localhost:27017/
DATABASE_NAME=RedCliffe_Labs

# AI API Keys
GEMINI_API_KEY=your-key-here

# Application
DEBUG=False
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📦 Building for Production

1. **Update environment variables**
```bash
DEBUG=False
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

2. **Use production WSGI server**
```bash
# FastAPI
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Flask
gunicorn wsgi:app -w 4 -b 0.0.0.0:5000
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Anand Raja M**
- GitHub: [@AnandRajaM](https://github.com/AnandRajaM)

## 🙏 Acknowledgments

- ReportLab for PDF generation
- Google Gemini for AI insights
- FastAPI and Flask communities

---

**Note**: This is a professional restructure of the original project. Old files preserved with `_old` suffix.
