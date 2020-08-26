import sys
import subprocess

from pymongo import MongoClient

from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection as MongoCollection

import toolbox as util


global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")

default_host = global_vars["SERVER"]["HOSTNAME"]
default_port = global_vars["SERVER"]["PORT"]

class MongoHandler:

    def __init__(self, host=default_host, port=default_port):
        self.host = host
        self.port = port

    def connect(self, host=None, port=None):
        if host is not None and port is not None:
            self._client = MongoClient(host, port)
            self.host, self.port = host, port
        
        else:
            self._client = MongoClient(self.host, self.port)

        self.db_list = self.get_db_objects()
        
    def get_db_objects(self):

        db_dict = {}

        for name in self._client.list_database_names():
            db = Database(client=self._client, name=name)
            db_dict[name] = db

        return db_dict


class Database(MongoDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.collections = self.get_collection_objects()
        
    def get_collection_objects(self):
        collection_dict = {}

        for name in self.list_collection_names():
            collection = Collection(database=self, name=name)
            collection_dict[name] = collection

        return collection_dict


class Collection(MongoCollection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    handler = MongoHandler()

    test_db = handler.db_list['test'].collections['test_db']

    print(test_db.count_documents({}))
