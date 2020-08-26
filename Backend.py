import sys
import subprocess

from pymongo import MongoClient
import toolbox as util


global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")


class MongoHandler:

    def __init__(self):
        self._client = MongoClient(global_vars["SERVER"]["HOSTNAME"])

        self.available_db_names: [] = self._get_available_db_names()

        self.current_chosen_database: str = "subscribe2pewdiepie"
        self.current_chosen_collection: str = "like_and_subscribe"

        self.current_collection_names: [str] = ["test_clction_name{}".format(num) for num in range(10)]
        self.current_collection_columns: [str] = ["test_field{}".format(num) for num in range(10)]

    def _get_available_db_names(self):
        return self._client.list_database_names()

    def select_database(self, database_name: str):
        # NOTE: Unfinished
        if database_name in self.available_db_names:
            print("Selected " + database_name)

    def select_collection(self, collection_name: str):
        # NOTE: Unfinished
        # Make sure a database has already been selected
        if self.current_chosen_database is None:
            raise Exception("No database has been selected yet.")
        
        if collection_name in self.current_collection_names:
            print("Yup")


    # region CRUD queries
    def create_query(self, query_data):
        print("Attmepting CREATE query..")

    def filter_query(self, query_data):
        print("Attmepting FILTER query..")

    def modify_query(self, query_data):
        print("Attmepting MODIFY query..")

    def delete_query(self, query_data):
        print("Attmepting DELETE query..")
    # endregion
            

class Database:
    def __init__(self):
        pass


class Collection:
    def __init__(self):
        pass


def run_cli(db: MongoHandler):
    print("\n\nCLI for testing Database class")
    print("You can run any command available by the pymongo module")
    print("example: db._client.list_database_names()")
    while True:
        user_input = input("> ")
        
        if user_input == "exit":
            sys.exit()

        if user_input == "clear":
            print("\n"*50)
            continue
        
        try: 
            exec("print(" + user_input + ")")
        except Exception as e:
            print("Encountered Exception")
            print(e)
            continue


def main():
    print("Attempting connection to database...")

    db = MongoHandler()

    print("Successfully Connected to database on {}:{}".format(global_vars['SERVER']['HOSTNAME'], global_vars['SERVER']['PORT']))

    run_cli(db)


if __name__ == "__main__":
    main()
