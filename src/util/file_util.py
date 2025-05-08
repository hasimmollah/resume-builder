import yaml


def load_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_yaml(path):
    with open(path, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)