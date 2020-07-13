from Database import Database


class EventListenerManager:
    def __init__(self, widget_objects: dict, db: Database):
        
        self.widget_objects: dict = widget_objects
        self.db = db
        self.__add_event_listeners()

    def __add_event_listeners(self):
        # Bind all database methods into frontend elements
        self.__add_manual_query_listener()

    def __add_manual_query_listener(self):
        query_text_field = self.widget_objects['manualQueryTextEdit']
        submit_button = self.widget_objects['submitQueryButton']

        query_text = ""

        def execute_manual_query(query_text=query_text):
            query_text = query_text_field.toPlainText()
            self.db.execute_manual_query(query_text)


        submit_button.clicked.connect(execute_manual_query)

