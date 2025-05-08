import logging
import re


from pdf.pdf_generator import PDFGenerator
from prompt_handler.manager import manage_prompt
from resume.resume_generator_prompt import prepare_prompt_data
from src import  get_path_from_project_root
from util.file_util import load_file

logger = logging.getLogger(__name__)

def clean_lines(text):
    # Define the patterns to skip
    skip_patterns = [
        r"\[.*?\]",        # Anything inside square brackets
        r"\(.*?\)",        # Anything inside parentheses
        r"\*\*.*?\*\*",    # Anything inside double asterisks
        r"\bSincerely\b",  # Lines with the word "Sincerely"
        r"\bHere’s\b",     # Lines with the word "Here’s"
        r"\bDear\b",       # Lines with the word "Dear"
        r"\bTo Whom\b",    # Lines with the phrase "To Whom"
        r"\bLet me know\b" # Lines with the phrase "Let me know"
    ]

    # Combine all patterns into a single regex
    combined_pattern = re.compile("|".join(skip_patterns))

    # Split into lines, filter based on the combined pattern, and rejoin
    filtered_lines = [
        line for line in text.splitlines()
        if not combined_pattern.search(line.strip())
    ]

    # Join the filtered lines back into a single string
    return "\n".join(filtered_lines)


def build_cover_letter(template_path, cover_letter_response):
    template = load_file(template_path)
    return template.format(
        cover_letter_response=cover_letter_response
    )
def execute_prompt(job_description:None):
    prompt_data = prepare_prompt_data(topic="cover_letter",
                                      topic_content="",
                                      job_description=job_description)
    cover_letter = clean_lines(manage_prompt(prompt_data))
    logger.info('cover letter \n' + cover_letter)
    return cover_letter

def generate_cover_letter(txt_path=get_path_from_project_root("resources/cover_letter"), output_path=get_path_from_project_root("outputs/CoverLetter-Hasim-Mollah-Java-JEE-Lead_Engineer.pdf"), prompt_mode =False, job_description=None):
    template_path = get_path_from_project_root("resources/cover-letter-template")

    if prompt_mode:
        cover_letter_response = execute_prompt(job_description)
    else:
        cover_letter_response = load_file(txt_path)


    cover_letter_final = build_cover_letter(template_path, cover_letter_response)
    # Read the text
    lines = [line.strip() for line in cover_letter_final.split("\n") if line.strip()]
    pdf_generator = PDFGenerator(pdf_path=output_path)
    # Print the list of lines
    for line in lines:
        # Add each line as a paragraph
        pdf_generator.add_calibri_style_paragraph(line)
        pdf_generator.add_spacer(1,6)
    pdf_generator.save()



