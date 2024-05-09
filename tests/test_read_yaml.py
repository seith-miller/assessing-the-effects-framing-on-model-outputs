import unittest
import yaml

class TestYAML(unittest.TestCase):
    def test_load_prompts(self):
        with open('data/input/prompts.yaml', 'r') as file:
            data = yaml.safe_load(file)
            for name, details in data.items():
                prompt = details['prompt']
                print(prompt)

if __name__ == '__main__':
    unittest.main()
