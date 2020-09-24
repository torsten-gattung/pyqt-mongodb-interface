import json
import sys
from io import StringIO
import contextlib


def json_to_dict(file_path: str):
    with open(file_path) as _file:
        return json.load(_file)


def save_as_json(file, data):
    with open(file, 'w') as output_file:
        json.dump(data, output_file, indent=4)


def convert_to(data_type, data):
    """
    Converts given data into type data_type

    :Parameters:

    data_type: (str) type.\_\_name\_\_

    data: Any

    :Returns:

    Data cast to given type


    :Raises:
    
    ValueError if conversion cannot be done
    """

    # Check if conversion is necessary
    if type(data).__name__ == data_type:
        return data

    converted_data = None

    ldict = locals()
    # This raises a ValueError when it can't convert given data
    exec(f'converted_data = ' + data_type + ' (data)', globals(), ldict)
    converted_data = ldict['converted_data']


    return converted_data


def print_dict(dict_):
    for key, value in dict_.items():
        print(f"{key}: {value}")
