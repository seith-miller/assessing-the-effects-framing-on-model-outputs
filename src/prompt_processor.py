from ai_interface import get_responses, process_prompts
from utilities import load_config, write_responses_to_yaml
from visualization import process_data, plot_data


def main():
    api_key = load_config()
    prompt_file = 'prompts.yaml'
    output_file = 'responses.yaml'
    
    # Load prompts and generate new responses
    prompts = process_prompts(prompt_file, api_key)
    responses = get_responses(prompts, api_key)
    write_responses_to_yaml(responses, output_file)
    print("response data has been written.")
    
    # Load the newly written responses and process them
    responses_data = process_prompts(output_file, api_key)  # Read the YAML file for responses
    true_counts, false_counts = process_data(responses_data)  # Process the data to count true/false responses

    plot_data(true_counts, false_counts)  # Plot the data using the counts
    print("Data has been visualized.")


if __name__ == "__main__":
    main()
