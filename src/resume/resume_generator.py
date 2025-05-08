

from src import get_path_from_project_root
from pdf.pdf_generator import PDFGenerator
from util.file_util import load_yaml

def chunk_list(lst, chunk_size):
    """Yield successive chunk_size-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def generate_pdf(pdf_path=get_path_from_project_root("outputs/Hasim-Mollah-Java-JEE-Lead_Engineer_CV.pdf"),
                 resume_data=None,
                 data_file=get_path_from_project_root("resources/resume_data.yaml")
                 ):
    defaults = load_yaml(data_file)
    name = resume_data.name or defaults['name']
    contact = resume_data.contact or defaults['contact']
    professional_summary = resume_data.professional_summary or defaults['professional_summary']
    keystrengths = resume_data.keystrengths or defaults['keystrengths']
    company_data = resume_data.company_data or defaults['company_data']
    certifications = resume_data.certifications or defaults['certifications']
    education = resume_data.education or defaults['education']

    pdf_generator = PDFGenerator(pdf_path=pdf_path)
    # Heading
    pdf_generator.add_header_paragraph(f"<b>{name}</b>")
    pdf_generator.add_center_style_paragraph(contact)
    pdf_generator.add_spacer(1, 5)

    # Professional Info
    pdf_generator.add_shaded_style_paragraph("Professional Summary")
    pdf_generator.add_calibri_style_paragraph(professional_summary)
    pdf_generator.add_spacer(1, 5)
    pdf_generator.add_shaded_style_paragraph("Key Strengths")
    # Bullet List

    pdf_generator.add_bullets(keystrengths)
    pdf_generator.add_spacer(1, 5)

    pdf_generator.add_shaded_style_paragraph("Employment History")

    for data in company_data:
        # First Row: Designation, Company, Start-End Date
        first_row = [
            pdf_generator.create_calibri_style_paragraph(data['designation']),
            pdf_generator.create_centre_align_style_paragraph(data['company']),
            pdf_generator.create_right_align_style_paragraph(data['start_end'])
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
            pdf_generator.create_calibri_style_paragraph("Skills"),
            pdf_generator.create_calibri_style_paragraph(skills_str)
        ]

        # Third Row: Responsibilities, Bullet points

        responsibilities = data['responsibilities']
        responsibility_rows = []
        first_label_added = False

        for chunk in chunk_list(responsibilities, 2):
            bullets = pdf_generator.make_bullets(chunk)
            if not first_label_added:
                label = pdf_generator.create_calibri_style_paragraph("Responsibilities")
                first_label_added = True
            else:
                label = pdf_generator.create_calibri_style_paragraph("")

            responsibility_rows.append([label, bullets])

        # Final table data including the previous rows
        table_data = [first_row, second_row] + responsibility_rows
        span_styles = [('SPAN', (1, i), (2, i)) for i in range(1, len(table_data))]

        # Combine the rows into a single list of rows for the table
        col_widths = [90, 380, 90]

        # Create the table with no borders
        pdf_generator.add_table(table_data,col_widths,[
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

        ] + span_styles)
        pdf_generator.add_spacer(1, 10)

    pdf_generator.add_shaded_style_paragraph("Certifications")

    pdf_generator.add_bullets(certifications)
    pdf_generator.add_spacer(1, 5)
    pdf_generator.add_shaded_style_paragraph("Education Summary")
    pdf_generator.add_bullet(education)

    # Save PDF
    pdf_generator.save()

if __name__ == "__main__":
    generate_pdf()