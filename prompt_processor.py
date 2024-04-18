import yaml
import openai
from openai import OpenAI

client = OpenAI()
import json
import configparser

def load_config():
    """Load configuration from config.ini file."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openai']['api_key']

def read_yaml_file(file_path):
    """Reads a YAML file and returns the content."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def write_responses_to_file(responses, output_file):
    """Writes the responses to a JSON file."""
    with open(output_file, 'w') as file:
        json.dump(responses, file, indent=4)

def submit_prompt_to_openai(prompt):
    """Submits a prompt to the OpenAI API and returns the response."""
    try:
        response = client.completions.create(model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150)
        return response.choices[0].text.strip()
    except openai.APIError as e:
        return f"Error: {str(e)}"

def process_prompts(file_path):
    """Processes each prompt in the YAML file, submits them to OpenAI, and saves the responses."""
    data = read_yaml_file(file_path)
    responses = {}

    for test_name, details in data.items():
        prompt = details.get('prompt') or details.get('question')
        response = submit_prompt_to_openai(prompt)
        responses[test_name] = {'response': response}

    return responses

def main():
    # api_key = load_config()
    input_file = 'prompts.yaml'
    output_file = 'output_responses.json'
    responses = process_prompts(input_file)
    write_responses_to_file(responses, output_file)
    print("Responses have been written to the output file.")

if __name__ == "__main__":
    main()
