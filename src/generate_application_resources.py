import argparse
import logging
import os
import sys
import time
from pathlib import Path

from src import  get_path_from_project_root
from resume.cover_letter_generator import generate_cover_letter
from resume.tailored_resume_generator import generate_resume
from job.job_extractor import extract_job_description_no_headless
from util.file_util import load_file

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__name__)

def generate_resources(output_path=get_path_from_project_root("outputs"), url= None, prompt_mode = True, job_description_path=get_path_from_project_root("resources/job-description")):

    job_description = load_file(job_description_path)
    #job-description
    if url:
        job_description =  extract_job_description_no_headless(url)
    generate_resume(output_path=Path(output_path).resolve() / "CV.pdf", prompt_mode =prompt_mode, job_description = job_description)
    generate_cover_letter(output_path=Path(output_path).resolve() / "CoverLetter.pdf", prompt_mode =prompt_mode, job_description=job_description)

if __name__ == "__main__":
    start_time = time.time()
    #url = "https://jobs.ashbyhq.com/caribou/354a2cf7-640b-43a4-b6f6-3da7be834ca6"
    parser = argparse.ArgumentParser(description="Generate tailored resume and cover letter.")

    # Adding optional arguments with default values
    parser.add_argument("--url", help="The URL of the job description", default=None)
    parser.add_argument("--output_path", help="The Path to generate resume & cover letter", default=get_path_from_project_root("outputs"))
    parser.add_argument("--job_description_path", help="Path to the job description file", default=get_path_from_project_root("resources/job-description"))
    parser.add_argument("--prompt_mode", choices=["True", "False"], default="True",
                        help="Mode of generation (default is 'True')")

    args = parser.parse_args()

    url = args.url
    prompt_mode = args.prompt_mode
    output_path = args.output_path
    job_description_path= args.job_description_path
    logger.info(f"\nurl= {url}")
    logger.info(f"\noutput_path= {output_path}")
    logger.info(f"\nprompt_mode= {prompt_mode}")
    logger.info(f"\njob_description_path= {job_description_path}")
    generate_resources(output_path=output_path, url=url, prompt_mode=prompt_mode, job_description_path=job_description_path)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"\nProgram completed in {elapsed_time:.2f} seconds.")
    #generate_resources()