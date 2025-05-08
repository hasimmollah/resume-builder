import logging
import sys

from exception import MissingJobDescriptionError, MissingPromptDataError
from model.data_classes import PromptData
from prompt_handler.creator import generate_prompt
from prompt_handler.executor import execute_prompt

logger = logging.getLogger(__name__)

def manage_prompt(prompt_data:PromptData):
    try:
        if not prompt_data:
            raise MissingPromptDataError()
        if not prompt_data.job_description:
            raise MissingJobDescriptionError
        return execute_prompt(generate_prompt(prompt_data))
    except (MissingPromptDataError, MissingJobDescriptionError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)