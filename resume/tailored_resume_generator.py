import re

from resume.resume_generator import generate_pdf
from resume.tailored_resume_parser import parse_experience_blocks, parse_resume


def generate_resume(input_path='../resources/resume.txt', output_path="../outputs/Hasim-Mollah-Java-JEE-Lead_Engineer_CV.pdf"):
    data = parse_resume(input_path)
    generate_pdf(output_path,
                 name=data['name'],
                 contact=data['contact'],
                 professional_summary=data['professional_summary'],
                 keystrengths=data['key_strengths'],
                 company_data=parse_experience_blocks(data['employment_history']),
                 certifications=data['certifications'],
                 education=data['education_summary'],
                 data_file="../resources/resume_data.yaml"
                 )