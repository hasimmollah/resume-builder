import logging
import time

from src import  get_path_from_project_root
from resume.cover_letter_generator import generate_cover_letter
from resume.tailored_resume_generator import generate_resume
from company.job_extractor import extract_job_description_no_headless
from util.file_util import load_file

logger = logging.getLogger(__name__)

def generate_resources(output_path=get_path_from_project_root("outputs"), url= None, prompt_mode = True):

    job_description = load_file(get_path_from_project_root("resources/job-description"))
    #job-description
    if url:
        job_description =  extract_job_description_no_headless(url)
    #generate_resume(output_path=output_path + "\Hasim-Mollah-Java-JEE-Lead_Engineer_CV.pdf", prompt_mode =prompt_mode, job_description = job_description)
    generate_cover_letter(output_path=output_path + "\CoverLetter-Hasim-Mollah-Java-JEE-Lead_Engineer.pdf", prompt_mode =prompt_mode, job_description=job_description)

if __name__ == "__main__":
    start_time = time.time()
    #url = "https://jobs.ashbyhq.com/caribou/354a2cf7-640b-43a4-b6f6-3da7be834ca6"
    url = None
    prompt_mode = True
    generate_resources(output_path="C:\\Users\hasim\Downloads\Job-Application\\bcg\sde2132", url=url, prompt_mode=prompt_mode)
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"\nProgram completed in {elapsed_time:.2f} seconds.")
    #generate_resources()