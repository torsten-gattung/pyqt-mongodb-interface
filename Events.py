from custom_exceptions import *
from PyQt5.QtWidgets import *
import re

from time import sleep


# region Base Classes

class EventListenerManager:
    def __init__(self, gui, db):
        
        self.gui = gui
        self.db = db

    def __add_event_listeners(self):
        raise UnimplementedMethodException("Method must be implemented in inheriting classes")


class MainWindowListener(EventListenerManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

        create_button.clicked.connect(self.gui.show_create_window)
        filter_button.clicked.connect(self.gui.show_filter_window)
        modify_button.clicked.connect(self.gui.show_modify_window)
        delete_button.clicked.connect(self.gui.show_delete_window)

    def __add_function_buttons_listeners(self):

        for button_id, button  in self.gui.widget_objects.items():
            # this RegEx catches all objects with id ~= "functionNumberButton"
            if re.match("^function.*Button$", button_id):
                self.__add_button_listener(button, button_id)

    def __add_edit_db_and_collection_buttons_listeners(self):

        edit_database_button = self.gui.widget_objects['editDatabaseButton']
        edit_collection_button = self.gui.widget_objects['editCollectionButton']

        edit_database_button.clicked.connect(self.gui.view_edit_db_window)
        edit_collection_button.clicked.connect(self.gui.view_edit_collection_window)


class DynamicPopupWindowListener(EventListenerManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__add_field_listeners()

    def __add_field_listeners(self):
        for widget in self.gui.fields_widget.children():
            
            expected_type = type(QLineEdit())
            
            if type(widget) == expected_type:
                widget.setText("This is development code, so I can put anything I want here")


# endregion Base Classes


class WelcomeWindowListener(EventListenerManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._host_field, self._port_field = self.__get_fields()

        self.__add_event_listeners()


    def __get_fields(self):
        _host_field: QLineEdit = self.gui.widget_objects['hostLineEdit']
        _port_field: QLineEdit = self.gui.widget_objects['portLineEdit']

        return _host_field, _port_field

    def __add_event_listeners(self):
        self.__add_run_button_listener()

    def __add_run_button_listener(self):
        self.gui.widget_objects['runButton'].clicked.connect(self.__run_button_on_click)

    def __check_field_values(self):
        
        self._host_field.setDisabled(True)
        self._port_field.setDisabled(True)

        return True


    def __run_button_on_click(self):

        # Check fields
        if not self.__check_field_values():
            raise BadFieldValueException("Invalid value entered in host field")

        # Attempt Connection

        # ???

        # Profit

        print("//{}:{}".format(self._host_field.text(), self._port_field.text()))

        self.gui.close()


# region Edit DB / Collection Window Listeners

class EditDatabaseWindowListener(EventListenerManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__add_event_listeners()

    def __add_event_listeners(self):
        self.__add_buttons()
        self.__add_line_edits()
        self.__add_labels()

    def __add_buttons(self):
        pass

    def __add_line_edits(self):
        pass

    def __add_labels(self):
        pass


class EditCollectionWindowListener(EventListenerManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__add_event_listeners()

    def __add_event_listeners(self):
        self.__add_buttons()
        self.__add_line_edits()
        self.__add_labels()

    def __add_buttons(self):
        pass

    def __add_line_edits(self):
        pass

    def __add_labels(self):
        pass


# endregion Edit DB / Collection Window Listeners


# region CRUD Window Listeners

class CreateWindowListener(DynamicPopupWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__add_button_listener()

    def __add_button_listener(self):
        self.gui.widget_objects['createButton'].clicked.connect(lambda: print("Created Item (fake)"))
        self.gui.widget_objects['createButton'].clicked.connect(self.__list_all_field_data)

    def __list_all_field_data(self):
        for widget in self.gui.fields_widget.children():

            if type(widget) == type(QLabel):
                print(field.text(), end="")

            if type(widget) == type(QLineEdit()):
                print(widget.text())


class FilterWindowListener(DynamicPopupWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__add_button_listener()

    def __add_button_listener(self):
        self.gui.widget_objects['filterButton'].clicked.connect(lambda: print("Filtered Item (fake)"))
        self.gui.widget_objects['filterButton'].clicked.connect(self.__list_all_field_data)

    def __list_all_field_data(self):
        for widget in self.gui.fields_widget.children():

            if type(widget) == type(QLabel):
                print(field.text(), end="")

            if type(widget) == type(QLineEdit()):
                print(widget.text())


class ModifyWindowListener(DynamicPopupWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__add_button_listener()

    def __add_button_listener(self):
        self.gui.widget_objects['updateButton'].clicked.connect(lambda: print("Updated Item (fake)"))
        self.gui.widget_objects['updateButton'].clicked.connect(self.__list_all_field_data)

    def __list_all_field_data(self):
        for widget in self.gui.fields_widget.children():

            if type(widget) == type(QLabel):
                print(field.text(), end="")

            if type(widget) == type(QLineEdit()):
                print(widget.text())


class DeleteWindowListener(DynamicPopupWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__add_button_listener()

    def __add_button_listener(self):
        self.gui.widget_objects['deleteButton'].clicked.connect(lambda: print("Deleted Item (fake)"))
        self.gui.widget_objects['deleteButton'].clicked.connect(self.__list_all_field_data)

    def __list_all_field_data(self):
        for widget in self.gui.fields_widget.children():

            if type(widget) == type(QLabel):
                print(field.text(), end="")

            if type(widget) == type(QLineEdit()):
                print(widget.text())

# endregion CRUD Window Listeners
