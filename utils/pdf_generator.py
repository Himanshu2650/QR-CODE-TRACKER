import csv
import pandas as pd
from fpdf import FPDF
from PIL import Image

def generate_checklist_pdf(csv_path, output_pdf):
    
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font('DejaVuSans', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.add_font('DejaVuSans', 'B', 'fonts/DejaVuSans-Bold.ttf', uni=True)
    
    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        for row in reader:
            
            location = str(row[0]).strip()
            checklist_text = str(row[1]).strip()

            if location and checklist_text and location.lower() != '':
                               
                pdf.set_font("DejaVuSans", 'B', 10)
                pdf.multi_cell(0, 10, f"Checklist for {location}", ln=True)

                pdf.set_font("DejaVuSans", '', 8)
                pdf.multi_cell(0, 8, f'"{checklist_text}"')
                pdf.ln(5)

        pdf.output(output_pdf)
    return output_pdf

    
def generate_map_pdf(image_path, output_pdf):
    pdf = FPDF()
    pdf.add_page()

    # Register font
    pdf.add_font('DejaVuSans', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVuSans", '', 14)

    # Title
    pdf.cell(200, 10, txt="Walk Route Map", ln=True, align='C')
    pdf.ln(10)

    try:
        img = Image.open(image_path)
        width, height = img.size
        aspect = height / float(width)
        pdf_width = 180
        pdf_height = pdf_width * aspect
        pdf.image(image_path, x=15, y=30, w=pdf_width, h=pdf_height)
    except Exception as e:
        pdf.set_font("DejaVuSans", '', 10)
        pdf.cell(200, 10, txt="⚠ Could not load map image.", ln=True)

    pdf.output(output_pdf)
    return output_pdf
