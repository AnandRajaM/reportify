from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet

import operations

pdfmetrics.registerFont(TTFont('SofiaPro', './Resources/sofiapro-light.ttf')) 

styles = getSampleStyleSheet()
styles['Normal'].fontName = 'SofiaPro'

def create_page_with_image(image_path):
    c = canvas.Canvas("./stack_pdfs/output.pdf", pagesize=letter)

    width, height = letter

    c.drawImage(image_path, 0, 0, width, height)
    c.setFont("SofiaPro", 18) 
    c.drawString(55, 640, "Uric Acid Test")


    c.setFont("SofiaPro", 12)
    c.drawString(55, 620, "sdddddddddddddddddvgsgdsggggggggggggggggggggggggggggggggggggggggggggggggg")
    c.drawStrings()
    
    c.save()


create_page_with_image("./Resources/diag_report.png")