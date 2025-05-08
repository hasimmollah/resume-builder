from resume.resume_generator_prompt import generate
from src import get_path_from_project_root
from resume.resume_generator import generate_pdf
from resume.tailored_resume_parser import parse_resume


def generate_resume(input_path=get_path_from_project_root("resources/resume"), output_path=get_path_from_project_root("outputs/CV.pdf"), prompt_mode=False, job_description = None):
    if prompt_mode is True:
        data = generate(job_description=job_description)
        generate_pdf(output_path,
                     data
                     )
    else:
        data = parse_resume(input_path)
        generate_pdf(output_path,
                     data,
                     data_file=get_path_from_project_root("resources/resume_data.yml")
                     )

