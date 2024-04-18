import unittest
from unittest.mock import patch, mock_open
import prompt_processor

class TestPromptProcessor(unittest.TestCase):

    def test_read_yaml_file(self):
        """Test reading YAML content from a file."""
        mock_yaml_content = """
        Logic_1_Unframed:
            question: "How much does the ice cream cost?"
        """
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('yaml.safe_load', return_value={'Logic_1_Unframed': {'question': "How much does the ice cream cost?"}}) as mock_yaml:
                result = prompt_processor.read_yaml_file('dummy_path.yaml')
                self.assertEqual(result, {'Logic_1_Unframed': {'question': "How much does the ice cream cost?"}})
                mock_yaml.assert_called()

    def test_submit_prompt_to_openai(self):
        """Test the submission of a prompt to the OpenAI API."""
        with patch('openai.resources.Completions.create') as mock_create:
            mock_create.return_value = {'choices': [{'text': 'Ice cream costs $0.05.'}]}
            response = prompt_processor.submit_prompt_to_openai("How much does the ice cream cost?", 'fake_api_key')
            self.assertEqual(response, 'Ice cream costs $0.05.')
            mock_create.assert_called_with(engine="text-davinci-002", prompt="How much does the ice cream cost?", max_tokens=150, api_key='fake_api_key')

    def test_write_responses_to_file(self):
        """Test writing responses to a JSON file."""
        mock_responses = {'Logic_1_Unframed': {'response': 'Ice cream costs $0.05.'}}
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('json.dump') as mock_json_dump:
                prompt_processor.write_responses_to_file(mock_responses, 'dummy_output.json')
                mock_file.assert_called_with('dummy_output.json', 'w')
                mock_json_dump.assert_called_with(mock_responses, mock_file(), indent=4)

# Main block to run the tests
if __name__ == '__main__':
    unittest.main()
