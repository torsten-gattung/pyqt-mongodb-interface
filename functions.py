import json

def load_global_variables():
    with open("GLOBAL_VARIABLES.json") as global_vars_as_json:

        global_vars_as_dict = json.load(global_vars_as_json)

        return global_vars_as_dict