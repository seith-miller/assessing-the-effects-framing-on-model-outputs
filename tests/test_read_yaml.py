# test_read_yaml.py
import yaml

def test_read_yaml():
    with open('prompts.yaml', 'r') as file:
        data = yaml.safe_load(file)
        print(data)

test_read_yaml()
