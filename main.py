import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.graphics import shapes
from reportlab.graphics.shapes import Polygon

import PyPDF2

from data_fetching import *
from pages import *


customer_name = "Sankar Roy"
booking_date= "2023-11-01 00:00:00 UTC"
patient_docs , booking_id = get_patient_docs(customer_name,booking_date)
test_names = [(item[0],) for item in patient_docs]

highlighted_tests=[]
Report_pages = []
c=0


for diagnostic_test in patient_docs:
    c+=1
    if diagnostic_test[0]=="Complete Blood Count (CBC)":
        filename = f"./stack_pdfs/report_page_{c}.pdf"
        print("RBC"+str(c)) 
        rbc_highlighted_tests = create_rbc_report_page(filename, A4, "./Resources/rbc_page.png", diagnostic_test,booking_id)
        highlighted_tests = merge_lists(highlighted_tests,rbc_highlighted_tests)
        Report_pages.append(filename)    

    elif diagnostic_test[0] == "Urine Routine and Microscopic Examination":
        filename = f"./stack_pdfs/report_page_{c}.pdf"
        print("URME"+str(c))
        urme_highlighted_tests=create_urme_report_page(filename, A4, "./Resources/urme_page.png", diagnostic_test,booking_id)
        highlighted_tests = merge_lists(highlighted_tests,urme_highlighted_tests)
        Report_pages.append(filename)
    
    else:
        print("val"+str(c))
        filename = f"./stack_pdfs/report_page_{c}.pdf"
        highlighted = create_report_page(filename, A4, "./Resources/2tests_report_page.png", diagnostic_test,booking_id)
        highlighted_tests = merge_lists(highlighted_tests,highlighted)
        Report_pages.append(filename)

create_body_report_page("./stack_pdfs/summary_report_page.pdf", A4, "./Resources/summary.png", highlighted_tests,test_names,booking_id)

Report_pages.insert(0, "./stack_pdfs/summary_report_page.pdf")

create_cover_pdf("./stack_pdfs/coverpage.pdf", letter, "./Resources/cover.png", customer_name)
Report_pages.insert(0, "./stack_pdfs/coverpage.pdf")

Report_pages.pop(6)
merge_pdfs("./stack_pdfs/final_report.pdf", *Report_pages)

print("Final report created successfully.")




