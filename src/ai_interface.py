import openai
from utilities import read_yaml_file


def submit_prompt_to_openai(prompt, api_key, model):
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
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            api_key=api_key
        )
        return response['choices'][0]['message']['content'].strip() if 'content' in response['choices'][0]['message'] else ""
    except openai.APIError as e:
        raise openai.APIError(f"API Error with {model}: {e}")
    except Exception as e:
        raise Exception(f"Unhandled exception with {model}: {e}")

def submit_verification_to_openai(response, correct_response, api_key, model):
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
    return submit_prompt_to_openai(verification_prompt, api_key, model)

def process_prompts(file_path, api_key, models):
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
    all_responses = {}
    for model in models:
        print("processing", model, "...")
        responses = {}
        for test_name, details in data.items():
            print("processing", test_name, "...")
            prompt = details['prompt']
            correct_response = details['correct_response']
            generated_response = submit_prompt_to_openai(prompt, api_key, model)
            verification_response = submit_verification_to_openai(generated_response, correct_response, api_key, model)
            responses[test_name] = {'model': model, 'response': generated_response, 'response_correct': verification_response}
        all_responses[model] = responses
        print("")
    return all_responses
