
class EventListenerManager:
    def __init__(self, widget_objects: dict):
        
        self.widget_objects: dict = widget_objects
        self.add_event_listeners()

    def add_event_listeners(self):

        # Import all functions from Database.py and bind them to the widgets
        # This is where all the event listeners will go. Below is an example.

        # Clicking the Create Button on the Main Tab will log "hello there" into the console
        self.widget_objects['createButton'].clicked.connect(lambda x: print("hello there"))