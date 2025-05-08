import os

from reportlab.lib import colors
from reportlab.lib import styles
from reportlab.lib.colors import navy
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from src import get_path_from_project_root
from src.pdf.table_builder import TableBuilder

pdfmetrics.registerFont(TTFont('CalibriLight', 'calibril.ttf'))




def create_table(data, col_widths=None, style=None):
    tb = TableBuilder()
    table_id, table = tb.create_table(data, col_widths, style)
    return table


class PDFGenerator:
    def __init__(self, pdf_path=get_path_from_project_root("outputs/CV.pdf"), author="Anonymous", title="Resume"):

        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        self.doc = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            leftMargin=20,
            rightMargin=20,
            topMargin=10,
            bottomMargin=0
        )
        self.title = title
        self.author = author
        self._setup()

    def _setup(self):
        self.styles = getSampleStyleSheet()
        self.calibri_style = ParagraphStyle(
            "CalibriNavy",
            parent=self.styles["Normal"],
            fontName='CalibriLight',
            fontSize=8,
            textColor=navy,
            spaceAfter=0, spaceBefore=0

        )
        self.right_align_style = ParagraphStyle(
            "right",
            parent=self.calibri_style,
            alignment=TA_RIGHT
        )
        self.centre_align_style = ParagraphStyle(
            "right",
            parent=self.calibri_style,
            alignment=TA_CENTER
        )

        self.header_style = ParagraphStyle(
            "Header",
            parent=self.calibri_style,
            fontSize=16,
            fontName='CalibriLight',
            alignment=TA_CENTER,
            spaceAfter=10
        )

        self.subheader_style = ParagraphStyle(
            "Subheader",
            parent=self.calibri_style,
            fontSize=11,
            spaceAfter=10
        )
        # Custom styles
        self.header = ParagraphStyle("Header", parent=self.header_style )
        self.centre_style = ParagraphStyle("Bullet", parent=self.calibri_style, alignment=TA_CENTER)
        self.shaded_style = ParagraphStyle("Shaded", parent=self.subheader_style, spaceAfter=2, backColor=colors.lightblue,
                                      borderPadding=3)

        self.dark_blue = colors.Color(0, 0, 0.3)
        self.make_bullet = lambda text: Paragraph(
            f'<font color="{self.dark_blue}" size="12.5">•</font>&nbsp;&nbsp;&nbsp;&nbsp;{text}',
            self.calibri_style
        )

        self.make_bullets = lambda items: [
            item for text in items for item in (
                self.make_bullet(text), Spacer(1, 2)
            )
        ]
        self.elements = []

    def create_paragraph(self, text, style):
        if not isinstance(text, str):
            text = str(text)
        return Paragraph(text, style)

    def create_calibri_style_paragraph(self, text):
        return self.create_paragraph(text, self.calibri_style)

    def create_centre_align_style_paragraph(self, text):
        return self.create_paragraph(text, self.centre_align_style)

    def create_right_align_style_paragraph(self, text):
        return self.create_paragraph(text, self.right_align_style)


    def add_table(self, data, col_widths=None, style=None):
        self.elements.append(create_table(data, col_widths, style))

    def add_paragraph(self, text, style):
        self.elements.append(self.create_paragraph(text, style))

    def add_header_paragraph(self, text):
        self.add_paragraph(text, self.header)

    def add_center_style_paragraph(self, text):
        self.add_paragraph(text, self.centre_style)

    def add_shaded_style_paragraph(self, text):
        self.add_paragraph(text, self.shaded_style)

    def add_calibri_style_paragraph(self, text):
        self.add_paragraph(text, self.calibri_style)

    def add_subheader_style_paragraph(self, text):
        self.add_paragraph(text, self.subheader_style)

    def add_spacer(self, width, height):
        self.elements.append(Spacer(width, height))

    def add_bullets(self, data):
        self.elements.extend(self.make_bullets(data))

    def make_bullets(self, data):
        self.make_bullets(data)

    def add_bullet(self, data):
        self.elements.append(self.make_bullet(
        data))

    def save(self):
        self.doc.build(self.elements)

# Example Usage
if __name__ == "__main__":
    pdf = PDFGenerator(title="My Report", author="John Doe")
    pdf.add_header_paragraph("This is a paragraph in the report.")
    pdf.save()
