from custom_exceptions import *
from PyQt5.QtWidgets import *
import re
import traceback

from time import sleep


# region Base Classes

class EventListener:
    def __init__(self, gui, db):

        self.gui = gui
        self.db = db

    def _add_event_listeners(self):
        raise UnimplementedMethodException(
            "Method must be implemented in inheriting classes")


class MainWindowListener(EventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_event_listeners()

    def _add_event_listeners(self):
        # Bind all database methods into frontend elements
        self._add_crud_buttons_listeners()
        self.add_function_button_listeners()
        self._add_edit_db_and_collection_buttons_listeners()

    def _add_crud_buttons_listeners(self):
        create_button = self.gui.widget_objects['createButton']
        filter_button = self.gui.widget_objects['filterButton']
        modify_button = self.gui.widget_objects['modifyButton']
        delete_button = self.gui.widget_objects['deleteButton']

        create_button.clicked.connect(self.gui.show_create_window)
        filter_button.clicked.connect(self.gui.show_filter_window)
        modify_button.clicked.connect(self.gui.show_modify_window)
        delete_button.clicked.connect(self.gui.show_delete_window)

    def add_function_button_listeners(self):

        for button_id, button in self.gui.widget_objects.items():
            # this RegEx catches all objects with id ~= "functionNumberButton"
            if re.match("^function.*Button$", button_id):
                self._add_function_button_listener(button, button_id)

    def _add_function_button_listener(self, button, button_name: str):
        """
        Helper for self.add_function_button_listeners
        """
        button.clicked.connect(
            lambda: self.gui.show_function_window(button_name, button))

    def _add_edit_db_and_collection_buttons_listeners(self):

        edit_database_button = self.gui.widget_objects['editDatabaseButton']
        edit_collection_button = self.gui.widget_objects['editCollectionButton']

        edit_database_button.clicked.connect(self.gui.show_edit_db_window)
        edit_collection_button.clicked.connect(self.gui.show_edit_collection_window)


class CRUDWindowListener(EventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _list_all_field_data(self):
        for widget in self.gui.fields_container.children():

            if type(widget) == type(QLabel):
                print(widget.text(), end="")

            if type(widget) == type(QLineEdit()):
                print(widget.text())


# endregion Base Classes


class WelcomeWindowListener(EventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._host_field, self._port_field = self._get_fields()
        self.run_button = self._get_run_button()

        self._create_event_listeners()

    def _get_fields(self):
        _host_field: QLineEdit = self.gui.widget_objects['hostLineEdit']
        _port_field: QLineEdit = self.gui.widget_objects['portLineEdit']

        return _host_field, _port_field

    def _get_run_button(self):
        return self.gui.widget_objects['runButton']

    def _create_event_listeners(self):
        self._add_run_button_listener()

    def _add_run_button_listener(self):
        self.run_button.clicked.connect(self._run_button_on_click)

    def _check_field_values(self):

        host_field_is_full = len(self._host_field.text()) > 0
        port_field_is_full = len(self._port_field.text()) > 0

        if host_field_is_full and port_field_is_full:

            self.gui.setDisabled(True)

            return

        else:
            raise BadFieldValueException(
                "Invalid values detected in Host/Port Fields")

    def _run_button_on_click(self):

        # Check fields
        try:
            self._check_field_values()

        except BadFieldValueException as e:
            print(e)

            return

        # Attempt Connection

        print("Connecting to //{}:{}".format(self._host_field.text(),
                                             self._port_field.text()))

        try:
            # BUG #5 Program will crash if connection cannot be established
            host = self._host_field.text()
            port = int(self._port_field.text())
            self.db.connect(host, port)

            print("Successfully connected to database")

        except Exception as e:
            print(f"Ran into exception while connecting to database: ", e)
            traceback.print_exc()

            return

        self.gui.start_program()


# region Edit DB / Collection Window Listeners

class DatabaseWindowListener(EventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.select_button = self._get_select_button()
        self.create_db_button = self._get_create_db_button()
        self.delete_db_button = self._get_delete_db_button()


        self._add_event_listeners()


    def _get_select_button(self):
        return self.gui.widget_objects['selectButton']

    def _get_create_db_button(self):
        return self.gui.widget_objects['createDatabaseButton']

    def _get_delete_db_button(self):
        return self.gui.widget_objects['deleteDatabaseButton']


    def _add_event_listeners(self):
        self._add_buttons()
        self._add_line_edits()
        self._add_labels()


    def _add_buttons(self):
        self.select_button.clicked.connect(self.select_button_onclick)
        self.create_db_button.clicked.connect(self.create_db_button_onclick)
        self.delete_db_button.clicked.connect(self.delete_db_button_onclick)


    def select_button_onclick(self):
        self.gui.switch_to_selected_database()

    def create_db_button_onclick(self):
        self.gui.create_new_database()

        # self.gui.update_database_list()

    def delete_db_button_onclick(self):
        self.gui.delete_selected_database()

        # self.gui.update_database_list()


    def _add_line_edits(self):
        pass


    def _add_labels(self):
        pass
    

class CollectionWindowListener(EventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.select_button = self._get_select_button()
        self.change_name_button = self._get_change_name_button()
        self.export_collection_button = self._get_export_button()
        self.create_collection_button = self._get_create_collection_button()
        self.drop_collection_button = self._get_drop_collection_button()

        self._add_event_listeners()


    def _add_event_listeners(self):
        self._add_buttons()
        self._add_line_edits()
        self._add_labels()


    def _add_buttons(self):
        self.select_button.clicked.connect(self.select_button_onclick)
        self.change_name_button.clicked.connect(self.change_name_button_onclick)
        self.export_collection_button.clicked.connect(self.export_collection_button_onclick)
        self.create_collection_button.clicked.connect(self.create_collection_button_onclick)
        self.drop_collection_button.clicked.connect(self.drop_collection_button_onclick)


    def _get_select_button(self):
        return self.gui.widget_objects['selectButton']

    def _get_change_name_button(self):
        return self.gui.widget_objects['changeCollectionNameButton']

    def _get_export_button(self):
        return self.gui.widget_objects['exportButton']

    def _get_create_collection_button(self):
        return self.gui.widget_objects['createCollectionButton']

    def _get_drop_collection_button(self):
        return self.gui.widget_objects['dropCollectionButton']


    def select_button_onclick(self):
        self.gui.switch_to_selected_collection()

    def change_name_button_onclick(self):
        self.gui.change_collection_name()

    def export_collection_button_onclick(self):
        self.gui.export_collection()

    def create_collection_button_onclick(self):
        self.gui.create_new_collection()

    def drop_collection_button_onclick(self):
        self.gui.drop_selected_collection()


    def _add_line_edits(self):
        pass


    def _add_labels(self):
        pass

# endregion Edit DB / Collection Window Listeners


# region CRUD Window Listeners

class CreateWindowListener(CRUDWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_button = self._get_create_button()

        self.set_button_listeners()

    def _get_create_button(self):
        return self.gui.widget_objects['createButton']

    def set_button_listeners(self):
        self.create_button.clicked.connect(self.gui.create_button_onclick)


class FilterWindowListener(CRUDWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_button_listener()

    def _add_button_listener(self):
        self.gui.widget_objects['filterButton'].clicked.connect(
            lambda: print("Filtered Item (fake)"))
        self.gui.widget_objects['filterButton'].clicked.connect(
            self._list_all_field_data)


class ModifyWindowListener(CRUDWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_button_listener()

    def _add_button_listener(self):
        self.gui.widget_objects['updateButton'].clicked.connect(
            lambda: print("Updated Item (fake)"))
        self.gui.widget_objects['updateButton'].clicked.connect(
            self._list_all_field_data)


class DeleteWindowListener(CRUDWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_button_listener()

    def _add_button_listener(self):
        self.gui.widget_objects['deleteButton'].clicked.connect(
            lambda: print("Deleted Item (fake)"))
        self.gui.widget_objects['deleteButton'].clicked.connect(
            self._list_all_field_data)


# endregion CRUD Window Listeners
