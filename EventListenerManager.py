from Database import Database
from FrontendLoader import Gui, MainWindow
from CustomException import UnimplementedMethodException
import re

class EventListenerManager:
    def __init__(self, gui: Gui, db: Database):
        
        self.gui = gui
        self.db = db

    def __add_event_listeners(self):
        raise UnimplementedMethodException("Method must be implemented in inheriting classes")


class MainWindowEventListenerManager(EventListenerManager):
    def __init__(self, gui: MainWindow, db: Database):
        super(MainWindowEventListenerManager, self).__init__(gui, db)

        self.__add_event_listeners()

    def __add_event_listeners(self):
        # Bind all database methods into frontend elements
        self.__add_manual_query_listener()
        self.__add_crud_buttons_listeners()
        self.__add_function_buttons_listeners()
        self.__add_edit_db_and_collection_buttons_listeners()

    def __add_manual_query_listener(self):
        query_text_field = self.gui.widget_objects['manualQueryTextEdit']
        submit_button = self.gui.widget_objects['submitQueryButton']

        query_text = ""

        def execute_manual_query(query_text=query_text):
            query_text = query_text_field.toPlainText()
            self.db.execute_manual_query(query_text)


        submit_button.clicked.connect(execute_manual_query)
    
    def __add_button_listener(self, button, button_name: str):
        button.clicked.connect(lambda: print("Clicked " + button_name))

    def __add_crud_buttons_listeners(self):
        create_button = self.gui.widget_objects['createButton']
        filter_button = self.gui.widget_objects['filterButton']
        modify_button = self.gui.widget_objects['modifyButton']
        delete_button = self.gui.widget_objects['deleteButton']

        #####

        # NOTE: query_data will be assigned from the popup windows created later
        query_data = ""

        ######

        def create_query(query_data=query_data):
            self.db.create_query(query_data)

        def filter_query(query_data=query_data):
            self.db.filter_query(query_data)

        def modify_query(query_data=query_data):
            self.db.modify_query(query_data)

        def delete_query(query_data=query_data):
            self.db.delete_query(query_data)

        #####

        create_button.clicked.connect(create_query)
        filter_button.clicked.connect(filter_query)
        modify_button.clicked.connect(modify_query)
        delete_button.clicked.connect(delete_query)

    def __add_function_buttons_listeners(self):

        for button_id, button  in self.gui.widget_objects.items():
            # this RegEx catches all objects with id ~= "functionNumberButton"
            if re.match("^function.*Button$", button_id):
                self.__add_button_listener(button, button_id)

    def __add_edit_db_and_collection_buttons_listeners(self):

        edit_database_button = self.gui.widget_objects['editDatabaseButton']
        edit_collection_button = self.gui.widget_objects['editCollectionButton']

        self.__add_button_listener(edit_database_button, "Edit Database Button")
        self.__add_button_listener(edit_collection_button, "Edit Collection Button")
