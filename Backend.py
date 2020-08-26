import sys
import subprocess

from pymongo import MongoClient
import toolbox as util


global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")


class MongoHandler:

    def __init__(self):
        self._client = MongoClient(global_vars["SERVER"]["HOSTNAME"])


class Database:
    def __init__(self):
        pass


class Collection:
    def __init__(self):
        pass


if __name__ == "__main__":
    print("\n\nRun main.py to launch the program\n\n")