import sys

import yaml


def load_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def load_yaml(path):
    try:
        with open(path, 'r', encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)