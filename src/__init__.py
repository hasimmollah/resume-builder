from pathlib import Path

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
