import os
import json

def load_data(filename, cls):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return [cls.from_dict(item) for item in json.load(f)]

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([item.to_dict() for item in data], f, indent=4)

def load_categories(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_categories(filename, categories):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=4)
