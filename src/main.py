from ai_interface import get_responses, process_prompts
from utilities import load_config, write_responses_to_yaml
from visualization import process_data, plot_data

def run_application():
    api_key = load_config()
    prompt_file = 'data/input/prompts.yaml'
    output_file = 'data/output/responses.yaml'
    
    # Load prompts and generate new responses
    responses_data = process_prompts(prompt_file, api_key)
    write_responses_to_yaml(responses_data, output_file)
    
    true_counts, false_counts = process_data(responses_data)
    plot_data(true_counts, false_counts)

def main():
    try:
        run_application()
        print("Processing complete. Data has been visualized.")
    except Exception as e:
        print(f"Error running the application: {e}")

if __name__ == "__main__":
    main()
