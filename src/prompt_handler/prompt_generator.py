from abc import abstractmethod, ABC
from dataclasses import dataclass

from exception import MissingJobDescriptionError
from model.data_classes import PromptData
from src import get_path_from_project_root

from util.file_util import load_yaml, load_file


def build_instructions(yaml_data, topic):
    common = yaml_data['instructions'].get('common', [])
    topic_specific = yaml_data['instructions'].get(topic, [])
    return '\n'.join(['- ' + line for line in topic_specific + common])


class PromptGenerator(ABC):
    prompt_data: PromptData

    def build_prompt(self) -> str:
        pass

    def __post_init__(self):
        if not self.prompt_data.job_description:
            raise MissingJobDescriptionError()

    @abstractmethod
    def generate_prompt(self) -> str:
        pass


class ResumePrompt(PromptGenerator):
    def __init__(self, prompt_data):
        self.prompt_data = prompt_data

    def generate_prompt(self) -> str:
        template_path = "resources/prompt-template"
        yaml_data = load_yaml(get_path_from_project_root("resources/instructions.yml"))
        # topic = "summary"  # Or dynamically based on your logic
        instructions = build_instructions(yaml_data, self.prompt_data.topic)

        if not self.prompt_data.job_description:
            self.prompt_data.job_description = load_file(get_path_from_project_root("resources/job-description"))
        template = load_file(template_path)
        return template.format(
            job_description=self.prompt_data.job_description,
            topic_to_rephrase=self.prompt_data.topic,
            topic_content_to_rephrase=self.prompt_data.topic_content,
            instructions=instructions
        )


class CoverLetterPrompt(PromptGenerator):
    def __init__(self, prompt_data):
        self.prompt_data = prompt_data

    def generate_prompt(self) -> str:
        template_path = "resources/cover-letter-prompt-template"
        template = load_file(template_path)
        cover_letter_response = self.prompt_data.job_description
        return template.format(
            cover_letter_response=cover_letter_response,
        )

