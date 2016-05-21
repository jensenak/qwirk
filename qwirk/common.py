import json

def jsonFromFile(file):
    with open(file) as f:
        return json.load(f)