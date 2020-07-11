import json

def load_json_file_as_dict(file_path: str):
    with open(file_path) as _file:
        return json.load(_file)
