import argparse
import traceback

from ai_interface import process_prompts
from utilities import load_config, read_yaml_file, write_responses_to_yaml
from visualization import  plot_data, plot_data

def parse_args():
    parser = argparse.ArgumentParser(description='Process and visualize model output data.')
    parser.add_argument('--process', action='store_true', help='Run data processing only.')
    parser.add_argument('--visualize', action='store_true', help='Run visualization only.')
    return parser.parse_args()

def run_application(process_flag, visualize_flag):
    api_key, models = load_config()
    prompt_file = 'data/input/prompts.yaml'
    output_file = 'data/output/responses.yaml'
    
    if process_flag or not (process_flag or visualize_flag):
        all_responses = {}
        for model in models:
            responses_data = process_prompts(prompt_file, api_key, [model])
            all_responses[model] = responses_data[model]
        write_responses_to_yaml(all_responses, output_file)

    if visualize_flag or not (process_flag or visualize_flag):
        responses_data = read_yaml_file(output_file)
        plot_data(responses_data)

def main():
    args = parse_args()
    try:
        run_application(args.process, args.visualize)
        print("Operation completed successfully.")
    except Exception as e:
        print(f"Error during operation: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()