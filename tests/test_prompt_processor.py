import unittest
from unittest.mock import patch, call
import prompt_processor

class TestPromptProcessor(unittest.TestCase):
    @patch('prompt_processor.process_prompts')
    @patch('prompt_processor.get_responses')
    @patch('prompt_processor.write_responses_to_yaml')
    @patch('prompt_processor.load_config')
    def test_main_flow(self, mock_load_config, mock_write_yaml, mock_get_responses, mock_process_prompts):
        mock_load_config.return_value = 'fake_api_key'
        mock_get_responses.return_value = {}
        mock_process_prompts.side_effect = [{}, {}]  # Assuming it's called twice with different results

        prompt_processor.main()

        # Assert process_prompts was called correctly
        calls = [
            call('prompts.yaml', 'fake_api_key'),
            call('responses.yaml', 'fake_api_key')
        ]
        mock_process_prompts.assert_has_calls(calls, any_order=False)

        # Assert other interactions
        mock_write_yaml.assert_called_once()
        mock_get_responses.assert_called_once()

if __name__ == '__main__':
    unittest.main()
