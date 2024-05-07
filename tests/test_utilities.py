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

if __name__ == '__main__':
    unittest.main()