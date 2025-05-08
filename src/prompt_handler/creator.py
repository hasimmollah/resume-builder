from model.data_classes import PromptData
from src import get_path_from_project_root
from util.file_util import load_yaml, load_file


def build_instructions(yaml_data, topic):
    common = yaml_data['instructions'].get('common', [])
    topic_specific = yaml_data['instructions'].get(topic, [])
    return '\n'.join(['- ' + line for line in topic_specific + common])



def generate_prompt(prompt_data:PromptData):
    # Usage
    template_path = get_path_from_project_root("resources/prompt-template")
    yaml_data = load_yaml(get_path_from_project_root("resources/instructions.yml"))
    #topic = "summary"  # Or dynamically based on your logic
    instructions = build_instructions(yaml_data, prompt_data.topic)
    template = load_file(template_path)
    return template.format(
        job_description=prompt_data.job_description,
        topic_to_rephrase=prompt_data.topic,
        topic_content_to_rephrase=prompt_data.topic_content,
        instructions=instructions
    )

if __name__ == "__main__":
    generate_prompt()