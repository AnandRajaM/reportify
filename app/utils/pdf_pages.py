"""
PDF Page Generation Utilities
This module contains functions to create different pages of the medical report
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Line, Polygon
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
import PyPDF2
from barcode import EAN13 
from barcode.writer import ImageWriter
from app.core.config import settings
import os


class PDFPageGenerator:
    """Handles generation of different PDF pages for medical reports"""
    
    def __init__(self):
        self.register_fonts()
        self.styles = getSampleStyleSheet()
        self.styles['Normal'].fontName = 'SofiaPro'
    
    def register_fonts(self):
        """Register custom fonts for PDF generation"""
        font_path = os.path.join(settings.RESOURCES_DIR, 'Fonts')
        
        fonts = {
            'SofiaPro': 'sofiapro-light.ttf',
            'EastmanBold': 'Eastman-bold.ttf',
            'EastmanRegular': 'Eastman-regular.ttf',
            'SofiaProBold': 'SofiaPro-Bold.ttf',
            'RobotoRegular': 'Roboto-Regular.ttf',
            'RobotoBold': 'Roboto-Bold.ttf'
        }
        
        for font_name, font_file in fonts.items():
            try:
                pdfmetrics.registerFont(
                    TTFont(font_name, f'./{font_path}/{font_file}')
                )
            except Exception as e:
                print(f"Warning: Could not register font {font_name}: {e}")
    
    def create_cover_page(self, filename: str, page_size, cover_image_path: str, 
                         customer_name: str):
        """
        Create the cover page of the report
        
        Args:
            filename: Output PDF filename
            page_size: Page size (e.g., A4)
            cover_image_path: Path to cover image
            customer_name: Patient name
        """
        c = canvas.Canvas(filename, pagesize=page_size)
        # TODO: Implement cover page design
        # This is a placeholder - actual implementation from pages.py
        c.save()
    
    def create_summary_page(self, filename: str, patient_data: dict):
        """Create summary page with key health metrics"""
        c = canvas.Canvas(filename, pagesize=A4)
        # TODO: Implement summary page
        c.save()
    
    def create_detailed_test_page(self, filename: str, test_data: dict):
        """Create detailed test results page"""
        c = canvas.Canvas(filename, pagesize=A4)
        # TODO: Implement detailed test page
        c.save()
    
    def merge_pdfs(self, pdf_list: list, output_filename: str):
        """
        Merge multiple PDF files into one
        
        Args:
            pdf_list: List of PDF file paths
            output_filename: Output merged PDF filename
        """
        pdf_merger = PyPDF2.PdfMerger()
        
        for pdf in pdf_list:
            pdf_merger.append(pdf)
        
        with open(output_filename, 'wb') as output_file:
            pdf_merger.write(output_file)
        
        pdf_merger.close()


# NOTE: The complete page generation logic from pages.py (746 lines) 
# should be migrated here. This is a skeleton structure.
# For now, keeping the original pages.py functionality intact.

pdf_generator = PDFPageGenerator()
