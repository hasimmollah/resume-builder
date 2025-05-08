import os
import sys
from pathlib import Path
from . import resume
from . import prompt_handler
from . import job
from . import model
from . import pdf

import logging

# Set up logging configuration once, in the __init__.py of the package
LOG_FILE = "app.log"
LOG_DIR = os.path.dirname(os.path.abspath(__file__))

# Create the logging directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE)),
        logging.StreamHandler()
    ]
)


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Start from the current file
current_file = Path(__file__).resolve()

# Traverse upwards to find the directory that contains 'src'
for parent in current_file.parents:
    if (parent / "src").exists():
        project_root = parent
        break
else:
    # If we can't find it, default to current working directory
    project_root = Path.cwd()

# Expose it for import
PROJECT_ROOT = project_root

# Utility function to get paths relative to the project root
def get_path_from_project_root(relative_path: str) -> Path:
    return PROJECT_ROOT / relative_path
