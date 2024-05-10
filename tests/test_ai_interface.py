import unittest
from unittest.mock import patch, MagicMock
from ai_interface import submit_prompt_to_openai, submit_verification_to_openai, process_prompts

# Import the specific classes needed for exception handling if required
from openai.error import APIError, AuthenticationError

class TestAIInterface(unittest.TestCase):

    @patch('openai.ChatCompletion.create')
    def test_submit_prompt_to_openai_success(self, mock_create):
        # Setup the mock to return a successful response
        mock_create.return_value = {
            'choices': [{'message': {'content': "Test response"}}]
        }
        
        # Call the function with a test prompt
        response = submit_prompt_to_openai("Test prompt", "fake_api_key")
        
        # Check if the function returns the expected response
        self.assertEqual(response, "Test response")
        mock_create.assert_called_once_with(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test prompt"}],
            max_tokens=150,
            api_key="fake_api_key"
        )

    @patch('ai_interface.submit_prompt_to_openai')
    def test_submit_verification_to_openai(self, mock_submit):
        # Setup the mock
        mock_submit.return_value = "true"
        
        # Call the function
        result = submit_verification_to_openai("response", "correct_response", "fake_api_key")
        
        # Check results
        self.assertEqual(result, "true")
        mock_submit.assert_called_with(
            "Does the following response: 'response' correctly answer the question with 'correct_response'? Respond with 'true' or 'false'.",
            "fake_api_key"
        )

    @patch('ai_interface.read_yaml_file')
    @patch('ai_interface.submit_prompt_to_openai')
    @patch('ai_interface.submit_verification_to_openai')
    def test_process_prompts(self, mock_verification, mock_submit, mock_read_yaml):
        # Setup mocks
        mock_read_yaml.return_value = {
            'test_prompt': {'prompt': "Test prompt", 'correct_response': "Test response"}
        }
        mock_submit.return_value = "Test response"
        mock_verification.return_value = "true"
        
        # Call process_prompts
        responses = process_prompts("dummy_file.yaml", "fake_api_key")
        
        # Assertions
        self.assertEqual(responses['test_prompt']['response_correct'], "true")
        mock_read_yaml.assert_called_once_with("dummy_file.yaml")
        mock_submit.assert_called_once()
        mock_verification.assert_called_once()

if __name__ == '__main__':
    unittest.main()
