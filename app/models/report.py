"""
Data models and schemas for the application
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class TestParameter(BaseModel):
    """Individual test parameter"""
    parameter_name: str
    value: float
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    status: Optional[str] = None  # normal, high, low


class PatientTest(BaseModel):
    """Patient test information"""
    test_name: str
    test_date: datetime
    parameters: List[TestParameter]


class PatientInfo(BaseModel):
    """Patient information"""
    customer_name: str
    booking_id: Optional[str] = None
    booking_date: datetime
    age: Optional[int] = None
    gender: Optional[str] = None
    contact: Optional[str] = None


class ReportRequest(BaseModel):
    """Request model for generating PDF report"""
    customer_name: str
    booking_date: str
    include_highlights: bool = True
    

class ReportResponse(BaseModel):
    """Response model for PDF report generation"""
    success: bool
    message: str
    report_path: Optional[str] = None
    booking_id: Optional[str] = None


class HealthData(BaseModel):
    """Complete health data model"""
    patient_info: PatientInfo
    tests: List[PatientTest]
    summary: Optional[str] = None


class JSONToPDFRequest(BaseModel):
    """Request to convert JSON data to PDF"""
    patient_data: Dict[str, Any]
    template_type: str = "standard"  # standard, detailed, summary
    include_barcode: bool = True
    
    
class PDFGenerationResponse(BaseModel):
    """Response after PDF generation"""
    success: bool
    message: str
    pdf_url: Optional[str] = None
    file_size: Optional[int] = None
    generated_at: datetime = Field(default_factory=datetime.utcnow)
