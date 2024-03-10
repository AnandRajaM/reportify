import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.graphics import shapes
from reportlab.graphics.shapes import Polygon

import PyPDF2

from operations import *


pdfmetrics.registerFont(TTFont('SofiaPro', './Resources/sofiapro-light.ttf')) 
styles = getSampleStyleSheet()




pdfmetrics.registerFont(TTFont('SofiaPro', './Resources/sofiapro-light.ttf')) 
pdfmetrics.registerFont(TTFont('EastmanBold','./Resources/Eastman-bold.ttf'))
pdfmetrics.registerFont(TTFont('EastmanRegular','./Resources/Eastman-regular.ttf'))
pdfmetrics.registerFont(TTFont('SofiaProBold','./Resources/SofiaPro-Bold.ttf'))
styles['Normal'].fontName = 'SofiaPro'

patient_report = [{"test_method":"HPLC","test_parameter_id":7051016,"parameter_name":"GLYCOSYLATED HEMOGLOBIN (HbA1c)","parameter_value":"6.1","is_highlighted":True,"lower_bound":"0","display_value":"< 5.7","upper_bound":"5.6","impression":"H","unit":"%","other_male_id":"438"},{"test_method":"","test_parameter_id":7052039,"parameter_name":"ESTIMATED AVERAGE GLUCOSE","parameter_value":"128.37","is_highlighted":False,"lower_bound":"","display_value":"Refer Table Below","upper_bound":"","impression":"N","unit":"mg/dL","other_male_id":"439"}]
patient_report1 = [{"test_method":"Urease","test_parameter_id":5100,"parameter_name":"BLOOD UREA","parameter_value":"13.4","is_highlighted":True,"lower_bound":"19","display_value":"19 - 44.1","upper_bound":"44.1","impression":"L","unit":"mg/dL","other_male_id":"448"},{"test_method":"Photometric","test_parameter_id":7052160,"parameter_name":"CREATININE","parameter_value":"0.8","is_highlighted":False,"lower_bound":"0.57","display_value":"0.57 - 1.11","upper_bound":"1.11","impression":"N","unit":"mg/dL","other_male_id":"85"},{"test_method":"Urease","test_parameter_id":5102,"parameter_name":"BUN","parameter_value":"6.26","is_highlighted":True,"lower_bound":"7.0","display_value":"7.0 - 18.7","upper_bound":"18.7","impression":"L","unit":"mg/dL","other_male_id":"154"},{"test_method":"","test_parameter_id":7049764,"parameter_name":"BUN/CREATININE RATIO","parameter_value":"7.82","is_highlighted":False,"lower_bound":"","display_value":"","upper_bound":"","impression":"N","unit":"","other_male_id":"450"},{"test_method":"","test_parameter_id":7052037,"parameter_name":"UREA / CREATININE RATIO","parameter_value":"16.75","is_highlighted":False,"lower_bound":"","display_value":"","upper_bound":"","impression":"N","unit":"","other_male_id":"927"},{"test_method":"Uricase","test_parameter_id":7052223,"parameter_name":"URIC ACID","parameter_value":"5.3","is_highlighted":False,"lower_bound":"2.6","display_value":"2.6 - 6.0","upper_bound":"6.0","impression":"N","unit":"mg/dL","other_male_id":"449"},{"test_method":"Arsenazo III","test_parameter_id":704380,"parameter_name":"CALCIUM Serum","parameter_value":"9.7","is_highlighted":False,"lower_bound":"8.4","display_value":"8.4 - 10.2","upper_bound":"10.2","impression":"N","unit":"mg/dL","other_male_id":"16"},{"test_method":"Photometric","test_parameter_id":7049766,"parameter_name":"PHOSPHORUS","parameter_value":"2.6","is_highlighted":False,"lower_bound":"2.3","display_value":"2.3 - 4.7","upper_bound":"4.7","impression":"N","unit":"mg/dL","other_male_id":"47"},{"test_method":"Potentiometric","test_parameter_id":7049767,"parameter_name":"SODIUM","parameter_value":"140","is_highlighted":False,"lower_bound":"136","display_value":"136 - 145","upper_bound":"145","impression":"N","unit":"mmol/L","other_male_id":"51"},{"test_method":"Potentiometric","test_parameter_id":7051486,"parameter_name":"POTASSIUM","parameter_value":"4","is_highlighted":False,"lower_bound":"3.5","display_value":"3.5 - 5.1","upper_bound":"5.1","impression":"N","unit":"mmol/L","other_male_id":"32"},{"test_method":"Photometric","test_parameter_id":7051776,"parameter_name":"CHLORIDE","parameter_value":"100","is_highlighted":False,"lower_bound":"98","display_value":"98 - 107","upper_bound":"107","impression":"N","unit":"mmol/L","other_male_id":"177"}]
patient_report2 = [{"test_method":"","test_parameter_id":7050020,"parameter_name":"Prothrombin Time","parameter_value":"9","is_highlighted":True,"lower_bound":"11","display_value":"11.0 - 15.0","upper_bound":"15","impression":"H","unit":"","other_male_id":"188"}]

def create_cover_pdf(filename, page_size, cover_image_path):
    c = canvas.Canvas(filename, pagesize=page_size)
    c.drawImage(cover_image_path, 0, 0, width=page_size[0], height=page_size[1])
    c.save()

def merge_pdfs(output_filename, *input_filenames):
    pdf_merger = PyPDF2.PdfMerger()
    for input_filename in input_filenames:
        pdf_merger.append(input_filename)
    with open(output_filename, 'wb') as output_file:
        pdf_merger.write(output_file)

def create_val_report_page(out_filename, page_size, report_png, diagnostic_test_data):
    c = canvas.Canvas(out_filename, pagesize=page_size)
    c.drawImage(report_png, 0, 0, width=page_size[0], height=page_size[1])

    c.setFont("EastmanBold", 18) 
    c.drawString(125, 688, diagnostic_test_data['parameter_name']+" Test".title())

    c.setFont("EastmanRegular", 12)
    paragraph = Paragraph(get_data(diagnostic_test_data['parameter_name']+" Test"), styles['Normal']) 
    paragraph.wrap(420, 280)
    paragraph.drawOn(c, 125, 680 - paragraph.height)

    c.setFont("EastmanBold", 17)
    c.drawString(45, 575,"Test Value:")
    c.setFont("SofiaProBold", 15)
    c.drawString(138, 575, diagnostic_test_data['parameter_value'] + " " + diagnostic_test_data['unit'])

    if diagnostic_test_data['parameter_value'] > diagnostic_test_data['upper_bound'] and diagnostic_test_data['is_highlighted']:
        c.setFont("SofiaProBold", 15)    
        r,g,b = 219,68,55
        c.setFillColorRGB(r/255, g/255, b/255)
        c.circle(450, 581, 5, stroke=0, fill=1)
        c.setStrokeColorRGB(r/255, g/255, b/255)
        c.circle(450, 581, 7, stroke=1, fill=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(460, 575, "High")

    elif diagnostic_test_data['parameter_value'] < diagnostic_test_data['lower_bound'] and diagnostic_test_data['is_highlighted']:
        c.setFont("SofiaProBold", 15)    
        r,g,b = 219,68,55
        c.setFillColorRGB(r/255, g/255, b/255)
        c.circle(450, 581, 5, stroke=0, fill=1)
        c.setStrokeColorRGB(r/255, g/255, b/255)
        c.circle(450, 581, 7, stroke=1, fill=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(460, 575, "Low")
    
    elif diagnostic_test_data['parameter_value'] > diagnostic_test_data['lower_bound'] and diagnostic_test_data['parameter_value'] < diagnostic_test_data['upper_bound'] and diagnostic_test_data['is_highlighted']:
        c.setFont("SofiaProBold", 15)    
        r,g,b = 30,207,58
        c.setFillColorRGB(r/255, g/255, b/255)
        c.circle(450, 581, 5, stroke=0, fill=1)
        c.setStrokeColorRGB(r/255, g/255, b/255)
        c.circle(450, 581, 7, stroke=1, fill=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(460, 575, "Normal")

    else:
        c.setFont("SofiaProBold", 15)    
        r,g,b = 248,215,122
        c.setFillColorRGB(r/255, g/255, b/255)
        c.circle(450, 581, 5, stroke=0, fill=1)
        c.setStrokeColorRGB(r/255, g/255, b/255)
        c.circle(450, 581, 7, stroke=1, fill=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(460, 575, "Borderline")


    c.setFillColorRGB(1, 1, 1)
    c.setFont("SofiaPro", 13)
    if diagnostic_test_data['lower_bound'] != '':
        c.drawString(145,504  , "<"+diagnostic_test_data['lower_bound'] + diagnostic_test_data['unit'] )
    if diagnostic_test_data['upper_bound'] != '':
        c.drawString(420,504  , diagnostic_test_data['upper_bound'] + diagnostic_test_data['unit'] + ">")
    if diagnostic_test_data['upper_bound'] != '' and diagnostic_test_data['lower_bound'] != '':
        try:
            c.drawString(270, 504, diagnostic_test_data['display_value'] + diagnostic_test_data['unit'])
        except:
            c.drawString(270, 504, diagnostic_test_data['lower_bound'] + " - "+diagnostic_test_data['upper_bound'] + diagnostic_test_data['unit'])



    if diagnostic_test_data['parameter_value'] > diagnostic_test_data['upper_bound']:
        c.drawImage("Resources/box.png",420,466,width=75,height=35,mask='auto')
        c.setFont("SofiaPro", 12)
        c.setFillColorRGB(1, 1, 1)
        c.drawString(430, 479, "You: "+ diagnostic_test_data['parameter_value'] )   
    elif diagnostic_test_data['parameter_value'] < diagnostic_test_data['lower_bound']:
        c.drawImage("Resources/box.png",150,466,width=75,height=35,mask='auto')
        c.setFont("SofiaPro", 12)
        c.setFillColorRGB(1, 1, 1)
        c.drawString(160, 479, "You: "+ diagnostic_test_data['parameter_value'] )
    elif diagnostic_test_data['parameter_value'] > diagnostic_test_data['lower_bound'] and diagnostic_test_data['parameter_value'] < diagnostic_test_data['upper_bound']:
        c.drawImage("Resources/box.png",290,466,width=75,height=35,mask='auto')
        c.setFont("SofiaPro", 12)
        c.setFillColorRGB(1, 1, 1)
        c.drawString(300, 479, "You: "+ diagnostic_test_data['parameter_value'] ) 

    if diagnostic_test_data['parameter_value'] > diagnostic_test_data['upper_bound'] or diagnostic_test_data['parameter_value'] < diagnostic_test_data['lower_bound']:
        c.setFont("EastmanBold", 17)
        c.setFillColorRGB(0,0,0)
        c.drawString(45, 435, "Possible Cause of abnormal results: ")
        c.setFont("EastmanRegular", 12)
        if diagnostic_test_data['parameter_value'] > diagnostic_test_data['upper_bound']:
            high_low = "high"
        else:
            high_low = "low"
        paragraphp = Paragraph(get_data_cause_para(diagnostic_test_data['parameter_name']+" Test",high_low), styles['Normal']) 
        paragraphp.wrap(480, 260)
        paragraphp.drawOn(c, 45, 420 - paragraph.height)
        causes = get_data_cause(diagnostic_test_data['parameter_name'],high_low)
        paragraph1 = Paragraph(causes[0], styles['Normal'])
        paragraph1.wrap(95, 40)
        paragraph1.drawOn(c, 110, 360 - paragraph1.height)
        paragraph2 = Paragraph(causes[1], styles['Normal'])
        paragraph2.wrap(95, 45)
        paragraph2.drawOn(c, 290, 360 - paragraph2.height)
        paragraph3 = Paragraph(causes[2], styles['Normal'])
        paragraph3.wrap(95, 40)
        paragraph3.drawOn(c, 455, 360 - paragraph3.height)

    if diagnostic_test_data['parameter_value'] > diagnostic_test_data['lower_bound'] and diagnostic_test_data['parameter_value'] < diagnostic_test_data['upper_bound'] :
        c.setFont("EastmanBold", 17)
        c.setFillColorRGB(0,0,0)
        c.drawString(45, 430, "Seems like your all good! ")
        c.setFont("EastmanRegular", 12)
        paragraphp = Paragraph(get_data_cause_para(diagnostic_test_data['parameter_name']+" Test","normal"), styles['Normal']) 
        paragraphp.wrap(480, 260)
        paragraphp.drawOn(c, 45, 375 - paragraph.height)
        causes = get_data_cause(diagnostic_test_data['parameter_name'],"normal")
        paragraph1 = Paragraph(causes[0], styles['Normal'])
        paragraph1.wrap(95, 40)
        paragraph1.drawOn(c, 110, 360 - paragraph1.height)
        paragraph2 = Paragraph(causes[1], styles['Normal'])
        paragraph2.wrap(95, 45)
        paragraph2.drawOn(c, 290, 360 - paragraph2.height)
        paragraph3 = Paragraph(causes[2], styles['Normal'])
        paragraph3.wrap(95, 40)
        paragraph3.drawOn(c, 455, 360 - paragraph3.height)

        
    if diagnostic_test_data['parameter_value'] < diagnostic_test_data['lower_bound'] or diagnostic_test_data['parameter_value'] > diagnostic_test_data['upper_bound']:
        if diagnostic_test_data['parameter_value'] > diagnostic_test_data['upper_bound']:
            high_low = "high"
        else:
            high_low = "low"
        c.setFont("EastmanBold", 18)
        c.setFillColorRGB(0,0,0)
        c.drawString(45, 255, "Consider these:")
        c.setFont("EastmanRegular", 12)
        paragraphp = Paragraph(get_data_consider(diagnostic_test_data['parameter_name']+" Test",high_low), styles['Normal'])
        paragraphp.wrap(480, 260)
        paragraphp.drawOn(c, 45, 258 - paragraph.height)



    c.save()

Report_pages = []
for index, diagnostic_test_data in enumerate(patient_report):
    if isinstance(diagnostic_test_data["parameter_value"],(int,float)) :
        filename = f"./stack_pdfs/report_page_{index}.pdf"
        create_val_report_page(filename, A4, "./Resources/diag_report.png", diagnostic_test_data)
        Report_pages.append(filename)
    elif isinstance(diagnostic_test_data["parameter_value"],str):
        filename = f"./stack_pdfs/report_page_{index}.pdf"
        create_val_report_page(filename, A4, "./Resources/diag_report.png", diagnostic_test_data)
        Report_pages.append(filename)


merge_pdfs("./stack_pdfs/final_report.pdf", "coverpage.pdf", *Report_pages)

print("Final report created successfully.")




