import re

from resume.cover_letter_generator import generate_cover_letter
from resume.tailored_resume_generator import generate_resume
from resume.tailored_resume_parser import parse_experience_blocks, parse_resume


def generate_resources(output_path="../outputs"):
    generate_resume(output_path=output_path + "\Hasim-Mollah-Java-JEE-Lead_Engineer_CV.pdf")
    generate_cover_letter(output_path=output_path + "\CoverLetter-Hasim-Mollah-Java-JEE-Lead_Engineer.pdf")
generate_resources(output_path="C:\\Users\hasim\Downloads\Job-Application\\thredd\sde21")