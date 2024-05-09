import unittest
from unittest.mock import mock_open, patch
from utilities import load_config, read_yaml_file


class TestUtilities(unittest.TestCase):
    
    def test_load_config(self):
        # Example test case for load_config
        api_key = load_config()
        self.assertIsNotNone(api_key)  # Assuming your config should return something

    def test_read_yaml_file(self):
        """Test reading YAML content from a file using a mock."""
        mock_yaml_content = """
        key: value
        list:
          - item1
          - item2
        """
        # Use mock_open to simulate opening a file that returns mock_yaml_content
        with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
            with patch('yaml.safe_load', return_value={'key': 'value', 'list': ['item1', 'item2']}) as mock_yaml:
                # The path given here doesn't matter because the file opening is mocked
                data = read_yaml_file('dummy_path.yaml')
                self.assertEqual(data, {'key': 'value', 'list': ['item1', 'item2']})
                mock_yaml.assert_called()

    def test_read_actual_yaml_file(self):
        """Test reading actual YAML content from the file."""
        # Define the path to your actual YAML file
        file_path = 'data/input/prompts.yaml'
        
        # Read data from the actual YAML file
        data = read_yaml_file(file_path)
        
        # Perform some basic checks to confirm that data is read correctly
        # For example, check that the data is a dictionary
        self.assertIsInstance(data, dict)
        
        # Check that certain expected keys are present in the data
        # This assumes your YAML contains these keys; adjust as appropriate
        expected_keys = ['History_1_Unframed', 'Math_1_Framed']
        for key in expected_keys:
            self.assertIn(key, data)

        # Optionally, check the contents of one of the entries
        # This is just an example; tailor it to fit the structure of your actual YAML data
        self.assertEqual(data['History_1_Unframed']['prompt'], "What was the date of D-day?")
        self.assertEqual(data['History_1_Unframed']['correct_response'], "Tuesday, 6 June 1944")

        for test_name, details in data.items():
            print(test_name)
            prompt = details['prompt']
            print(prompt)


if __name__ == '__main__':
    unittest.main()