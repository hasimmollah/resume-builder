import os

from reportlab.lib.colors import navy
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_cover_letter(txt_path='../resources/cover_letter.txt', output_path='../outputs/CoverLetter-Hasim-Mollah-Java-JEE-Lead_Engineer.pdf'):
    # Read the text
    with open(txt_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Setup PDF document
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    calibri_style = ParagraphStyle(
        "CalibriNavy",
        parent=styles["Normal"],
        fontName='CalibriLight',
        fontSize=8,
        textColor=navy,
        spaceAfter=0, spaceBefore=0

    )
    elements = []

    # Add each line as a paragraph
    for line in lines:
        elements.append(Paragraph(line, calibri_style))
        elements.append(Spacer(1, 6))

    doc.build(elements)


