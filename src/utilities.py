import configparser
import yaml

def load_config():
    """
    Load configuration from the config.ini file.

    Returns:
    str: The API key stored under the 'openai' section.

    Raises:
    KeyError: If the 'api_key' is not found under the 'openai' section.
    configparser.Error: If the config file has issues or the section is missing.
    """
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    try:
        api_key = config['openai']['api_key']
        models = config['openai']['models'].split(', ')
        return api_key, models
    except KeyError as e:
        raise KeyError(f"Missing key in configuration: {e}")
    except configparser.Error as e:
        raise configparser.Error(f"Configuration file error: {e}")

def read_yaml_file(file_path):
    """
    Reads a YAML file and returns the parsed data.
    
    Args:
    file_path (str): The path to the YAML file to be read.

    Returns:
    dict: The content of the YAML file loaded as a dictionary.
    
    Raises:
    FileNotFoundError: If the YAML file cannot be found.
    yaml.YAMLError: If the YAML file contains invalid YAML.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")

def write_responses_to_yaml(responses, output_file):
    """
    Writes the given dictionary of responses to a YAML file.

    Args:
    responses (dict): A dictionary containing the responses to write.
    output_file (str): The path to the output file where the data will be written.

    Raises:
    IOError: If there is an issue writing to the file.
    """
    try:
        with open(output_file, 'w') as file:
            yaml.dump(responses, file, allow_unicode=True, default_flow_style=False)
    except IOError as e:
        raise IOError(f"Error writing to file {output_file}: {e}")
