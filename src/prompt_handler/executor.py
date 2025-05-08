import json

import requests
import os

def extract_response(professional_summary):
    json_str = professional_summary.text

    # Parse the string into a Python dictionary
    data = json.loads(json_str)

    # Access the 'response' key
    response_text = data.get("response")
    return response_text

def execute_prompt(prompt=""):
    api_url = os.getenv("MODEL_API_URL", "http://localhost:11434/api/generate")
    model = os.getenv("MODEL_NAME", "gemma3:1b")
    response = requests.post(
        api_url,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return extract_response(response)