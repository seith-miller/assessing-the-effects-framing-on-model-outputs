import yaml
import openai
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

def write_responses_to_yaml(responses, output_file):
    """Writes the responses to a YAML file, adding a 'true' field to each."""
    # Enhance each response in the dictionary with a 'true' field
    for key in responses:
        responses[key]['true'] = ""  # Add a blank 'true' field to each response

    with open(output_file, 'w') as file:
        yaml.dump(responses, file, allow_unicode=True, default_flow_style=False)

def submit_prompt_to_openai(prompt, api_key):
    """Submits a prompt to the OpenAI API using the ChatCompletion endpoint and returns the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Ensure this is the correct model name
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            api_key=api_key
        )
        # Correctly accessing the response text from the chat model
        text_response = response['choices'][0]['message']['content'].strip() if 'content' in response['choices'][0]['message'] else ""
        return text_response
    except openai.APIError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        # Catching any other exceptions that may occur and returning a string that includes their message
        return f"Unhandled exception: {str(e)}"


def process_prompts(file_path, api_key):
    """Processes each prompt in the YAML file, submits them to OpenAI, and saves the responses."""
    data = read_yaml_file(file_path)
    responses = {}

    for test_name, details in data.items():
        prompt = details.get('prompt') or details.get('question')
        response = submit_prompt_to_openai(prompt, api_key)
        responses[test_name] = {'response': response}

    return responses

def main():
    api_key = load_config()
    input_file = 'prompts.yaml'
    output_file = 'responses.yaml'
    responses = process_prompts(input_file, api_key)
    write_responses_to_yaml(responses, output_file)
    print("Responses have been written to the output file.")

if __name__ == "__main__":
    main()
