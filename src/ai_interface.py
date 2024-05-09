import itertools
import openai
from utilities import read_yaml_file


def submit_prompt_to_openai(prompt, api_key):
    """
    Submits a text prompt to the OpenAI API using the ChatCompletion endpoint and returns the response.

    Args:
    prompt (str): The text prompt to be submitted.
    api_key (str): The API key used for authenticating with OpenAI.

    Returns:
    str: The text response from OpenAI API.

    Raises:
    openai.APIError: If there's an API error during the request.
    Exception: If an unexpected error occurs during the request.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # This needs to be checked for accuracy and updated as necessary.
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            api_key=api_key
        )
        return response['choices'][0]['message']['content'].strip() if 'content' in response['choices'][0]['message'] else ""
    except openai.APIError as e:
        raise openai.APIError(f"API Error: {e}")
    except Exception as e:
        raise Exception(f"Unhandled exception: {e}")

def get_responses(prompts, api_key):
    """
    Generates responses for each prompt using the OpenAI API.

    Args:
    prompts (dict): A dictionary containing prompt details with keys for 'prompt' and 'correct_response'.
    api_key (str): The API key used for authenticating with OpenAI.

    Returns:
    dict: A dictionary with the prompt name as keys and the API's response and correctness as values.

    Raises:
    KeyError: If required keys are missing from the prompt details.
    """
    responses = {}
    for prompt_name, prompt_details in prompts.items():
        try:
            prompt_text = prompt_details['prompt']
            correct_response = prompt_details['correct_response']
        except KeyError as e:
            print(f"Missing key {e} for prompt {prompt_name}, skipping...")
            continue
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_text,
            max_tokens=150,
            api_key=api_key
        )
        response_text = response.choices[0].text.strip()
        response_correct = 'true' if response_text == correct_response else 'false'
        responses[prompt_name] = {'response': response_text, 'response_correct': response_correct}
    return responses

def submit_verification_to_openai(response, correct_response, api_key):
    """
    Submits a verification prompt to OpenAI to determine if a response is correct.

    Args:
    response (str): The response to be verified.
    correct_response (str): The correct response for comparison.
    api_key (str): The API key used for authenticating with OpenAI.

    Returns:
    str: The result of the verification, 'true' or 'false'.

    Raises:
    openai.APIError: If there's an API error during the request.
    Exception: If an unexpected error occurs during the request.
    """
    verification_prompt = f"Does the following response: '{response}' correctly answer the question with '{correct_response}'? Respond with 'true' or 'false'."
    return submit_prompt_to_openai(verification_prompt, api_key)

def process_prompts(file_path, api_key):
    """
    Processes each prompt in the YAML file, submits them to OpenAI, evaluates, and saves the responses.

    Args:
    file_path (str): The path to the YAML file containing the prompts.
    api_key (str): The API key used for authenticating with OpenAI.

    Returns:
    dict: A dictionary with the test names as keys and their responses and correctness verification as values.

    Raises:
    FileNotFoundError: If the YAML file cannot be found or read.
    yaml.YAMLError: If the YAML file contains invalid YAML.
    """
    data = read_yaml_file(file_path)
    responses = {}
    for test_name, details in data.items():
        prompt = details['prompt']
        correct_response = details['correct_response']
        generated_response = submit_prompt_to_openai(prompt, api_key)
        verification_response = submit_verification_to_openai(generated_response, correct_response, api_key)
        responses[test_name] = {'response': generated_response, 'response_correct': verification_response}
    return responses
