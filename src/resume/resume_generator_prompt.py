import logging

from model.data_classes import PromptData, ResumeData
from src import get_path_from_project_root
from prompt_handler.manager import manage_prompt

import re

from util.file_util import load_yaml

logger = logging.getLogger(__name__)

defaults = load_yaml(get_path_from_project_root("resources/resume_data.yaml"))

def cleaned_lines(input):
    #clean_response = re.sub(r"\[.*?]|\(.*?\)", "", input).strip()
    striped_line = [re.sub(r'\*\*', '', point) for point in re.findall(r'\*\s+(.*)', input)]
    filtered_bullet_points = [
        point for point in striped_line
        if not re.match(r'^(Okay|Here’s|Response)', point) and not re.search(r'[\[\(].*?[\]\)]', point)
    ]
    return filtered_bullet_points


def top_n_with_numbers(lines, max_lines=10):
    # Separate lines with numbers and without numbers
    with_numbers = [line for line in lines if re.search(r'\d', line)]
    without_numbers = [line for line in lines if not re.search(r'\d', line)]

    # Prioritize lines with numbers, then fill with remaining lines if needed
    top_n = with_numbers[:max_lines] + without_numbers[:max_lines - len(with_numbers)]
    return top_n

def get_professional_summary(job_description=None):
    prompt_data = prepare_prompt_data(topic="professional_summary",
                        topic_content=defaults['professional_summary'],
                        job_description=job_description)

    professional_summary = manage_prompt(prompt_data)
    logger.info('professional summary \n' + professional_summary)

    professional_summary_resp = re.sub(r"^(\*\*.*?\*\*).*\n?", "", professional_summary, flags=re.MULTILINE)
    return professional_summary_resp

def get_key_strengths(job_description=None):
    prompt_data = prepare_prompt_data(topic="keystrengths",
                                      topic_content=defaults['keystrengths'],
                                      job_description=job_description)
    key_strengths = manage_prompt(prompt_data)
    logger.info('keystrengths \n' + key_strengths)
    return top_n_with_numbers(cleaned_lines(key_strengths))
def prepare_prompt_data(topic = "",
    topic_content = "",
    job_description = ""):
    prompt_data = PromptData()
    setattr(prompt_data, "topic", topic)
    setattr(prompt_data, "topic_content", topic_content)
    setattr(prompt_data, "job_description", job_description)
    return prompt_data

def get_companies(job_description=None):
    company_data = defaults['company_data']
    additional_instructions = []
    companies = []
    current_company = None

    for index, data in enumerate(company_data):
        logger.info('========================================\n')
        logger.info(data['designation'] + ' ' + data['company'] + '\n')
        current_company = {
            'designation': data['designation'],
            'company': data['company'],
            'start_end': data['start_end'],
            'responsibilities': []
        }
        responsibilities = data['responsibilities']
        formatted_text = '\n'.join(f"- {line}" for line in responsibilities)
        if index < 2:
            additional_instructions.append(
                "Output must be read like a bullet points not a bio or narrative, number of bullet points should NOT MORE THAN 10, each point should be within 1-2 lines, dense with quantifiable achievements include each points from experience.")
        else:
            additional_instructions.append(
                "Output must be read like a bullet points not a bio or narrative, number of bullet points should NOT MORE THAN 5, each point should be within 1-2 lines, dense with quantifiable achievements include each points from experience.")
        prompt_data = prepare_prompt_data(topic="responsibilities",
                                          topic_content=formatted_text,
                                          job_description=job_description)
        tailored_responsibility = manage_prompt(prompt_data)
        logger.info(tailored_responsibility)
        if index < 2:
            current_company['responsibilities'].extend(top_n_with_numbers(cleaned_lines(tailored_responsibility)))
        else:
            current_company['responsibilities'].extend(top_n_with_numbers(cleaned_lines(tailored_responsibility), 5))

        companies.append(current_company)
    return companies


def generate(job_description=None):
    professional_summary_resp = get_professional_summary(job_description)
    key_strengths = get_key_strengths(job_description)
    companies = get_companies(job_description)
    resume_data = ResumeData()

    setattr(resume_data, "name", defaults['name'])
    setattr(resume_data, "contact", defaults['contact'])
    setattr(resume_data, "professional_summary", professional_summary_resp)
    setattr(resume_data, "keystrengths", key_strengths)
    setattr(resume_data, "company_data", companies)
    setattr(resume_data, "certifications", defaults['certifications'])
    setattr(resume_data, "education", defaults['education'])

    return resume_data


if __name__ == "__main__":
    generate()