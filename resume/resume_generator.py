import os

from reportlab.lib.colors import navy
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import yaml  # or json
from typing import Optional, List, Dict

def chunk_list(lst, chunk_size):
    """Yield successive chunk_size-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

# Load default values
def load_defaults(file_path="../resources/resume_data.yaml"):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

pdfmetrics.registerFont(TTFont('CalibriLight', 'calibril.ttf'))
# Create document
def generate_pdf(pdf_path="../outputs/Hasim-Mollah-Java-JEE-Lead_Engineer_CV.pdf",
                 name=None,
                 contact=None,
                 professional_summary=None,
                 keystrengths: Optional[List[str]] = None,
                 company_data: Optional[List[Dict]] = None,
                 certifications: Optional[List[str]] = None,
                 education: Optional[str] = None,
                 data_file="../resources/resume_data.yaml"
                 ):
    defaults = load_defaults(data_file)
    name = name or defaults['name']
    contact = contact or defaults['contact']
    professional_summary = professional_summary or defaults['professional_summary']
    keystrengths = keystrengths or defaults['keystrengths']
    company_data = company_data or defaults['company_data']
    certifications = certifications or defaults['certifications']
    education = education or defaults['education']
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=20,
        rightMargin=20,
        topMargin=10,
        bottomMargin=0
    )
    styles = getSampleStyleSheet()
    calibri_style = ParagraphStyle(
        "CalibriNavy",
        parent=styles["Normal"],
        fontName='CalibriLight',
        fontSize=8,
        textColor=navy,
        spaceAfter=0, spaceBefore=0

    )

    right_align_style = ParagraphStyle(
        "right",
        parent=calibri_style,
        alignment=TA_RIGHT
    )
    centre_align_style = ParagraphStyle(
        "right",
        parent=calibri_style,
        alignment=TA_CENTER
    )

    header_style = ParagraphStyle(
        "Header",
        parent=calibri_style,
        fontSize=16,
        fontName='CalibriLight',
        alignment=TA_CENTER,
        spaceAfter=10
    )

    subheader_style = ParagraphStyle(
        "Subheader",
        parent=calibri_style,
        fontSize=11,
        spaceAfter=10
    )
    # Custom styles
    header = ParagraphStyle("Header", parent=header_style, )
    centre_style = ParagraphStyle("Bullet", parent=calibri_style, alignment=TA_CENTER)
    shaded_style = ParagraphStyle("Shaded", parent=subheader_style, spaceAfter=2, backColor=colors.lightblue,
                                  borderPadding=3)

    dark_blue = colors.Color(0, 0, 0.3)
    make_bullet = lambda text: Paragraph(
        f'<font color="{dark_blue}" size="12.5">•</font>&nbsp;&nbsp;&nbsp;&nbsp;{text}',
        calibri_style
    )

    make_bullets = lambda items: [
        item for text in items for item in (
            make_bullet(text), Spacer(1, 2)
        )
    ]

    # Build content
    elements = []


    # Heading
    elements.append(Paragraph(f"<b>{name}</b>", header))
    elements.append(Paragraph(
        contact,
        centre_style))
    elements.append(Spacer(1, 5))
    # Professional Info
    elements.append(Paragraph("Professional Summary", shaded_style))
    elements.append(Paragraph(professional_summary, calibri_style))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("Key Strengths", shaded_style))
    # Bullet List

    elements.extend(make_bullets(keystrengths))
    elements.append(Spacer(1, 5))

    elements.append(Paragraph("Employment History", shaded_style))

    for data in company_data:
        # First Row: Designation, Company, Start-End Date
        first_row = [
            Paragraph(data['designation'], calibri_style),
            Paragraph(data['company'], centre_align_style),
            Paragraph(data['start_end'], right_align_style),
        ]

        # Second Row: Skills, Comma-separated skills
        skills = data.get('skills')

        # If missing or empty, try to fetch from defaults based on company + designation match
        if not skills:
            for default_entry in defaults.get('company_data', []):
                if (default_entry.get('company') == data.get('company') and
                        default_entry.get('designation') == data.get('designation')):
                    skills = default_entry.get('skills')
                    break

        # Join into string if still not None
        skills_str = ', '.join(skills) if skills else ''

        second_row = [
            Paragraph("Skills", calibri_style),
            Paragraph(skills_str, calibri_style)
        ]

        # Third Row: Responsibilities, Bullet points

        responsibilities = data['responsibilities']
        responsibility_rows = []
        first_label_added = False

        for chunk in chunk_list(responsibilities, 2):
            bullets = make_bullets(chunk)
            if not first_label_added:
                label = Paragraph("Responsibilities", calibri_style)
                first_label_added = True
            else:
                label = Paragraph("", calibri_style)

            responsibility_rows.append([label, bullets])

        # Final table data including the previous rows
        table_data = [first_row, second_row] + responsibility_rows
        span_styles = [('SPAN', (1, i), (2, i)) for i in range(1, len(table_data))]

        # Combine the rows into a single list of rows for the table
        col_widths = [90, 380, 90]

        # Create the table with no borders
        table = Table(table_data, colWidths=col_widths)  # Adjust colWidths as needed
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),  # First row, first column: LEFT alignment
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # First row, second column: CENTER alignment
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('LEFTPADDING', (0, 1), (0, 1), 6),  # Increase left padding for second row's first column
            ('LEFTPADDING', (1, 1), (1, 1), -60),
            ('LEFTPADDING', (0, 2), (0, 2), 6),  # Increase left padding for second row's first column
            ('LEFTPADDING', (1, 2), (1, -1), -30),
            ('RIGHTPADDING', (1, 1), (1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),

        ] + span_styles))

        elements.append(table)
        elements.append(Spacer(1, 10))

    elements.append(Paragraph("Certifications", shaded_style))

    elements.extend(make_bullets(certifications))
    elements.append(Spacer(1, 5))
    elements.append(Paragraph("Education Summary", shaded_style))

    elements.append(make_bullet(
        education))

    # Save PDF
    doc.build(elements)