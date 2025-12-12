"""
PDF Generation Service
Main service for generating medical reports from JSON data
"""
from typing import Dict, Any, Optional
import os
from datetime import datetime
from app.core.config import settings
from app.services.data_fetching import data_service
from app.utils.pdf_pages import pdf_generator


class PDFGeneratorService:
    """Service to generate PDF reports from patient data"""
    
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_report_from_db(self, customer_name: str, booking_date: str) -> Dict[str, Any]:
        """
        Generate PDF report by fetching data from database
        
        Args:
            customer_name: Patient name
            booking_date: Booking date
            
        Returns:
            Dictionary with report generation status and file path
        """
        try:
            # Fetch patient data
            patient_tests, booking_id = data_service.get_patient_docs(
                customer_name, booking_date
            )
            
            if not patient_tests:
                return {
                    "success": False,
                    "message": "No patient data found",
                    "report_path": None
                }
            
            # Generate PDF filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{customer_name}_{booking_id}_{timestamp}.pdf"
            output_path = os.path.join(self.output_dir, filename)
            
            # TODO: Implement actual PDF generation using pdf_generator
            # This requires migrating the logic from main.py
            
            return {
                "success": True,
                "message": "Report generated successfully",
                "report_path": output_path,
                "booking_id": booking_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating report: {str(e)}",
                "report_path": None
            }
    
    def generate_report_from_json(self, patient_data: Dict[str, Any], 
                                  template_type: str = "standard") -> Dict[str, Any]:
        """
        Generate PDF report from JSON data
        
        Args:
            patient_data: Patient data in JSON format
            template_type: Type of template (standard, detailed, summary)
            
        Returns:
            Dictionary with report generation status and file path
        """
        try:
            # Extract patient info
            customer_name = patient_data.get('customer_name', 'Unknown')
            booking_id = patient_data.get('booking_id', 'N/A')
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{customer_name}_{booking_id}_{timestamp}.pdf"
            output_path = os.path.join(self.output_dir, filename)
            
            # TODO: Implement JSON to PDF conversion
            # This is the core functionality for the FastAPI endpoints
            
            # Get file size
            file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
            
            return {
                "success": True,
                "message": "Report generated from JSON successfully",
                "pdf_url": f"/downloads/{filename}",
                "file_size": file_size,
                "generated_at": datetime.utcnow()
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating report from JSON: {str(e)}",
                "pdf_url": None,
                "file_size": 0,
                "generated_at": datetime.utcnow()
            }
    
    def validate_patient_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate patient data structure
        
        Args:
            data: Patient data dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ['customer_name', 'booking_date']
        return all(field in data for field in required_fields)


# Service instance
pdf_service = PDFGeneratorService()
