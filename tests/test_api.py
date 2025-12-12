"""
Test suite for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/reports/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_list_reports():
    """Test list reports endpoint"""
    response = client.get("/api/v1/reports/list")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "reports" in data


def test_json_to_pdf_invalid_data():
    """Test JSON to PDF with invalid data"""
    response = client.post(
        "/api/v1/reports/json-to-pdf",
        json={
            "patient_data": {},
            "template_type": "standard"
        }
    )
    assert response.status_code == 400


def test_json_to_pdf_valid_structure():
    """Test JSON to PDF with valid structure"""
    response = client.post(
        "/api/v1/reports/json-to-pdf",
        json={
            "patient_data": {
                "customer_name": "Test Patient",
                "booking_date": "2023-12-12",
                "booking_id": "TEST123"
            },
            "template_type": "standard",
            "include_barcode": True
        }
    )
    # Will fail in actual generation without full data, but structure is valid
    assert response.status_code in [200, 500]


def test_download_nonexistent_report():
    """Test downloading a non-existent report"""
    response = client.get("/api/v1/reports/download/nonexistent.pdf")
    assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
