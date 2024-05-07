import unittest
from visualization import process_data

class TestVisualization(unittest.TestCase):
    
    def test_process_data_all_true(self):
        """Test processing of data where all responses are true."""
        data = {'prompt1_Framed': {'response_correct': 'true'},
                'prompt2_Unframed': {'response_correct': 'true'}}
        expected_true_counts = {'Framed': 1, 'Unframed': 1}
        expected_false_counts = {'Framed': 0, 'Unframed': 0}
        true_counts, false_counts = process_data(data)
        self.assertEqual(true_counts, expected_true_counts)
        self.assertEqual(false_counts, expected_false_counts)

    def test_process_data_all_false(self):
        """Test processing of data where all responses are false."""
        data = {'prompt1_Framed': {'response_correct': 'false'},
                'prompt2_Unframed': {'response_correct': 'false'}}
        expected_true_counts = {'Framed': 0, 'Unframed': 0}
        expected_false_counts = {'Framed': 1, 'Unframed': 1}
        true_counts, false_counts = process_data(data)
        self.assertEqual(true_counts, expected_true_counts)
        self.assertEqual(false_counts, expected_false_counts)

    def test_process_data_mixed_responses(self):
        """Test processing of data with a mix of true and false responses."""
        data = {'prompt1_Framed': {'response_correct': 'true'},
                'prompt2_Framed': {'response_correct': 'false'},
                'prompt3_Unframed': {'response_correct': 'true'},
                'prompt4_Unframed': {'response_correct': 'false'}}
        expected_true_counts = {'Framed': 1, 'Unframed': 1}
        expected_false_counts = {'Framed': 1, 'Unframed': 1}
        true_counts, false_counts = process_data(data)
        self.assertEqual(true_counts, expected_true_counts)
        self.assertEqual(false_counts, expected_false_counts)

if __name__ == '__main__':
    unittest.main()
