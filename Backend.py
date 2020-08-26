import sys
import subprocess

from pymongo import MongoClient

from pymongo.database import Database as MongoDatabase
from pymongo.collection import Collection as MongoCollection

import toolbox as util


global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")


class MongoHandler:
    def __init__(self):
        self._client = MongoClient(global_vars["SERVER"]["HOSTNAME"])

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
