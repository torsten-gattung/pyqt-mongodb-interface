import json
import sys
from io import StringIO
import contextlib


def json_to_dict(file_path: str):
    with open(file_path) as _file:
        return json.load(_file)

