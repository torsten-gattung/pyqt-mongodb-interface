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

        self._client: MongoClient = None

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

        self.update_local_dbs()


    def update_local_dbs(self):
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


    def switch_collection(self, collection_name):
        if collection_name in self.current_db.collection_dict.keys():
            self.current_collection = self.current_db.collection_dict[collection_name]
            print(f"Switched to collection '{collection_name}'")

        else:
            raise ClientAndServerOutOfSyncException("Collection list and mongo server are out of sync!")


    def get_field_template(self):
        """
        Returns an element in a collection to show the schema of the collection
        """
        if self.current_collection is None:
            raise CollectionNotChosenYetException("Must choose collection before get_field_template can be called")
        
        else:
            return self.current_collection.get_field_template()


    def get_current_db_doc_count(self):
        count_ = 0

        for collection in self.current_db.collection_dict.values():
            count_ += collection.count_documents({})

        return count_


    def create_new_database(self, db_name, template):

        # TODO: implement usage of templates

        self._client[db_name].create_collection("place_holder_collection")
        print("Database has been created!")

        self.update_local_dbs()

    def drop_selected_database(self, db_name):
        self._client.drop_database(db_name)

        self.update_local_dbs()


    def update_current_db_collections(self):
        """
        Update current_db to refer to database with updated collection names
        """

        current_db_name = self.current_db.name
        self.current_db = self.db_dict[current_db_name]

    def change_collection_name(self, selected_collection, new_collection_name):
        self.current_db.collection_dict[selected_collection].rename(new_collection_name)

        self.update_local_dbs()
        self.update_current_db_collections()


    def create_new_collection(self, new_collection_name):
        self.current_db.create_collection(name=new_collection_name)

        self.update_local_dbs()
        self.update_current_db_collections()


    def drop_selected_collection(self, selected_collection, is_last=False):
        self.current_db.drop_collection(selected_collection)

        if is_last:
            self.current_db = None
            self.current_collection = None

        self.update_local_dbs()


class Database(MongoDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.collection_dict = self.get_collection_objects()

    def get_collection_objects(self):
        collection_dict = {}

        for name in self.list_collection_names():
            collection = Collection(database=self, name=name)
            collection_dict[name] = collection

        return collection_dict


class Collection(MongoCollection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_field_template(self):
        """
        Returns an element in the collection to its schema
        """
        template_ = self.find_one()
        return template_


if __name__ == "__main__":
    handler = MongoHandler()
    handler.connect("localhost", 27017)

    test_db = handler.db_dict['test'].collection_dict['test_db']

    print(test_db.get_field_template())

    print(test_db.count_documents({}))
