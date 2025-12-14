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

# Importing custom modules
from data_fetching import *
from pages import *


# # Customer name and booking date to generate report
customer_name = "Sankar Roy"
# booking_date= "2023-11-01 00:00:00 UTC"


# # Fetch patient documents and booking ID
# patient_docs , booking_id = get_patient_docs(customer_name,booking_date)
patient_docs , booking_id = useSampleData()
test_names = [(item[0],) for item in patient_docs]


# Initialize lists to store highlighted tests and report pages
highlighted_tests=[]
Report_pages = []
c=0


# Iterate through each diagnostic test in patient documents
for diagnostic_test in patient_docs:
    c+=1
    if diagnostic_test[0]=="Complete Blood Count (CBC)":
        filename = f"./outputs/report_page_{c}.pdf"
        print("RBC"+str(c)) 
        rbc_highlighted_tests = create_rbc_report_page(filename, A4, "./reportGen/Resources/rbc_page.png", diagnostic_test,booking_id)
        # Merge highlighted tests into the main list
        highlighted_tests = merge_lists(highlighted_tests,rbc_highlighted_tests)
        # Append report page filename to the list
        Report_pages.append(filename)    

    elif diagnostic_test[0] == "Urine Routine and Microscopic Examination":
        filename = f"./outputs/report_page_{c}.pdf"
        print("URME"+str(c))
        urme_highlighted_tests=create_urme_report_page(filename, A4, "./reportGen/Resources/urme_page.png", diagnostic_test,booking_id)
        # Merge highlighted tests into the main list
        highlighted_tests = merge_lists(highlighted_tests,urme_highlighted_tests)
        # Append report page filename to the list
        Report_pages.append(filename)
    
    else:
        print("val"+str(c))
        filename = f"./outputs/report_page_{c}.pdf"
        highlighted = create_report_page(filename, A4, "./reportGen/Resources/2tests_report_page.png", diagnostic_test,booking_id)
        # Merge highlighted tests into the main list
        highlighted_tests = merge_lists(highlighted_tests,highlighted)
        # Append report page filename to the list
        Report_pages.append(filename)

# Create summary report with body image- page
create_body_report_page("./outputs/summary_report_page.pdf", A4, "./reportGen/Resources/summary.png", highlighted_tests,test_names,booking_id)
Report_pages.insert(0, "./outputs/summary_report_page.pdf")

# Create cover page with customer name
create_cover_pdf("./outputs/coverpage.pdf", letter, "./reportGen/Resources/cover.png", customer_name)
Report_pages.insert(0, "./outputs/coverpage.pdf")

print("Final report created successfully.")



merged_pdf_path = f"./outputs/{customer_name}_{booking_id}_final_report.pdf"
new = merge_pdfs(merged_pdf_path, *Report_pages)
print(f"Merged PDF saved at: {merged_pdf_path}")
