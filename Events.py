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


class DynamicPopupWindowListener(EventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self._add_field_listeners()

    def _add_field_listeners(self):
        for widget in self.gui.fields_container.children():

            expected_type = type(QLineEdit())

            if type(widget) == expected_type:
                widget.setText("placeholder")

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

        self._add_event_listeners()

    def _get_select_button(self):
        return self.gui.widget_objects['selectButton']

    def _add_event_listeners(self):
        self._add_buttons()
        self._add_line_edits()
        self._add_labels()

    def _add_buttons(self):
        self.select_button.clicked.connect(self.select_button_onclick)

    def select_button_onclick(self):

        selected_db = self.gui.get_selected_database()

        if selected_db is not None:
            self.db.switch_db(selected_db)
            self.gui.update_collection_list()
            self.gui.update_information_labels()

            self.gui.close()


    def _add_line_edits(self):
        pass

    def _add_labels(self):
        pass


class CollectionWindowListener(EventListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.select_button = self._get_select_button()

        self._add_event_listeners()

    def _get_select_button(self):
        return self.gui.widget_objects['selectButton']

    def _add_event_listeners(self):
        self._add_buttons()
        self._add_line_edits()
        self._add_labels()

    def _add_buttons(self):
        self.select_button.clicked.connect(self.select_button_onclick)

    def select_button_onclick(self):
        selected_collection = self.gui.get_selected_collection()

        if selected_collection is not None:
            self.db.switch_collection(selected_collection)

            self.gui.update_information_labels()

            self.gui.close()

    def _add_line_edits(self):
        pass

    def _add_labels(self):
        pass


# endregion Edit DB / Collection Window Listeners


# region CRUD Window Listeners

class CreateWindowListener(DynamicPopupWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_button_listener()

    def _add_button_listener(self):
        self.gui.widget_objects['createButton'].clicked.connect(
            lambda: print("Created Item (fake)"))
        self.gui.widget_objects['createButton'].clicked.connect(
            self._list_all_field_data)


class FilterWindowListener(DynamicPopupWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_button_listener()

    def _add_button_listener(self):
        self.gui.widget_objects['filterButton'].clicked.connect(
            lambda: print("Filtered Item (fake)"))
        self.gui.widget_objects['filterButton'].clicked.connect(
            self._list_all_field_data)


class ModifyWindowListener(DynamicPopupWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_button_listener()

    def _add_button_listener(self):
        self.gui.widget_objects['updateButton'].clicked.connect(
            lambda: print("Updated Item (fake)"))
        self.gui.widget_objects['updateButton'].clicked.connect(
            self._list_all_field_data)


class DeleteWindowListener(DynamicPopupWindowListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._add_button_listener()

    def _add_button_listener(self):
        self.gui.widget_objects['deleteButton'].clicked.connect(
            lambda: print("Deleted Item (fake)"))
        self.gui.widget_objects['deleteButton'].clicked.connect(
            self._list_all_field_data)


# endregion CRUD Window Listeners
