from Database import Database


class EventListenerManager:
    def __init__(self, widget_objects: dict, db: Database):
        
        self.widget_objects: dict = widget_objects
        self.db = db
        self.__add_event_listeners()

    def __add_event_listeners(self):
        # Bind all database methods into frontend elements
        self.__add_manual_query_listener()
        self.__add_crud_buttons_listeners()

    def __add_manual_query_listener(self):
        query_text_field = self.widget_objects['manualQueryTextEdit']
        submit_button = self.widget_objects['submitQueryButton']

        query_text = ""

        def execute_manual_query(query_text=query_text):
            query_text = query_text_field.toPlainText()
            self.db.execute_manual_query(query_text)


        submit_button.clicked.connect(execute_manual_query)

    def __add_crud_buttons_listeners(self):
        create_button = self.widget_objects['createButton']
        filter_button = self.widget_objects['filterButton']
        modify_button = self.widget_objects['modifyButton']
        delete_button = self.widget_objects['deleteButton']

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
