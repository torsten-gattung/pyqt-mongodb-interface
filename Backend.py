import sys
import subprocess
import traceback

from pymongo import MongoClient

from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection as MongoCollection

from custom_exceptions import *

import toolbox as util


global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")

default_host = global_vars["SERVER"]["HOSTNAME"]
default_port = global_vars["SERVER"]["PORT"]

class MongoHandler:

    def __init__(self, host=default_host, port=default_port):
        self.host = host
        self.port = port
        
        self.current_db = None
        self.current_collection = None

    def connect(self, host=None, port=None):
        if host is not None and port is not None:
            self._client = MongoClient(host, port)
            self.host, self.port = host, port
        
        else:
            self._client = MongoClient(self.host, self.port)

        self.continue_init()

    def continue_init(self):
        self.db_dict = self.get_db_objects()
        self.db_names = self.db_dict.keys()

    def get_db_objects(self):

        db_dict = {}

        for name in self._client.list_database_names():
            db = Database(client=self._client, name=name)
            db_dict[name] = db

        return db_dict

    def switch_db(self, db_name):

        if db_name in self.db_names:
            self.current_db = self.db_dict[db_name]
            self.current_collection = None
            print(f"Switched to '{self.current_db.name}' database")

        else:
            raise ClientAndServerOutOfSyncException("Database list and mongo server are out of sync!")
            traceback.print_exc()

    def switch_collection(self, collection_name):
        if collection_name in self.current_db.list_collection_names():
            self.current_collection = self.current_db.collection_dict[collection_name]
            print(f"Switched to collection '{collection_name}'")

        else:
            raise ClientAndServerOutOfSyncException("Collection list and mongo server are out of sync!")
            traceback.print_exc()


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

    test_db = handler.db_dict['test'].collections['test_db']

    print(test_db.count_documents({}))
