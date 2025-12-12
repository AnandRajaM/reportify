"""
FastAPI endpoints for report generation
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Dict, Any
import os

from app.models.report import (
    ReportRequest, 
    ReportResponse, 
    JSONToPDFRequest, 
    PDFGenerationResponse
)
from app.services.pdf_generator import pdf_service
from app.core.config import settings


router = APIRouter()


@router.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """
    Generate PDF report from database
    
    - **customer_name**: Patient's name
    - **booking_date**: Booking date in ISO format
    - **include_highlights**: Whether to include highlighted tests
    """
    result = pdf_service.generate_report_from_db(
        customer_name=request.customer_name,
        booking_date=request.booking_date
    )
    
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    
    return ReportResponse(**result)


@router.post("/json-to-pdf", response_model=PDFGenerationResponse)
async def convert_json_to_pdf(request: JSONToPDFRequest):
    """
    Convert JSON patient data to PDF report
    
    - **patient_data**: Complete patient data in JSON format
    - **template_type**: Template type (standard, detailed, summary)
    - **include_barcode**: Whether to include barcode
    """
    # Validate patient data
    if not pdf_service.validate_patient_data(request.patient_data):
        raise HTTPException(
            status_code=400, 
            detail="Invalid patient data. Required fields: customer_name, booking_date"
        )
    
    result = pdf_service.generate_report_from_json(
        patient_data=request.patient_data,
        template_type=request.template_type
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    
    return PDFGenerationResponse(**result)


@router.get("/download/{filename}")
async def download_report(filename: str):
    """
    Download generated PDF report
    
    - **filename**: Name of the PDF file to download
    """
    file_path = os.path.join(settings.OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        path=file_path,
        media_type='application/pdf',
        filename=filename
    )


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Reportify PDF Generator",
        "version": settings.APP_VERSION
    }


@router.get("/reports/list")
async def list_reports():
    """List all generated reports"""
    try:
        reports = []
        output_dir = settings.OUTPUT_DIR
        
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if f.endswith('.pdf')]
            for file in files:
                file_path = os.path.join(output_dir, file)
                stat = os.stat(file_path)
                reports.append({
                    "filename": file,
                    "size": stat.st_size,
                    "created_at": stat.st_ctime,
                    "download_url": f"/api/v1/reports/download/{file}"
                })
        
        return {
            "total": len(reports),
            "reports": reports
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
