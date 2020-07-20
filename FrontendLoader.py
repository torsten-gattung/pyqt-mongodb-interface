from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import utility as util
from EventListenerManager import *
from Database import *


global_vars = util.load_json_file_as_dict("GLOBAL_VARIABLES.json")


class Gui(QMainWindow):

    # Stores all loaded widgets for easy access throughout program
    widget_objects = {}

    def __init__(self, widget_ids: dict, gui_file_path: str):
        super(Gui, self).__init__()
        uic.loadUi(gui_file_path, self)

        self.gui_file_path = gui_file_path

        # holds all widget ids as strings: { QWidgetType: [id1, id2, ..] }
        self.widget_ids: dict = widget_ids

        self.__load_all_qt_objects()

    def __load_all_qt_objects(self):
        print("\nLoading all GUI elements...")
        for object_type, id_list in self.widget_ids.items():
            for object_id in id_list:
                exec("self.widget_objects[object_id] = self.findChild(" + object_type + ", object_id)")

        print("Successfully loaded all GUI elements")


class PopupWindow(Gui):
    def __init__(self, widget_ids, gui_file_path, parent_gui, db):
        super(PopupWindow, self).__init__(widget_ids, gui_file_path)
        self.parent_gui = parent_gui
        self.db = db

    
    def closeEvent(self, a0):
        self.parent_gui.setDisabled(False)  # return 'focus' to parent
        self.hide()
        return super().closeEvent(a0)


class DynamicPopupWindow(PopupWindow):
    def __init__(self, widget_ids, gui_file_path, parent_gui, db, disable_field_edit=False, fields=[]):
        super(DynamicPopupWindow, self).__init__(widget_ids, gui_file_path, parent_gui, db)

        # self.collection_columns: [str] = self.db.current_collection_columns
        self.collection_columns = fields

        self.fields_widget: QWidget = self.widget_objects['fieldsWidget']
        self.__add_fields()

        self.event_listener_manager = DynamicPopupWindowListener(self, self.db)

    def __create_qobjects(self):
        labels = [QLabel(col_name) for col_name in self.collection_columns]
        field_widgets = [QLineEdit() for _ in self.collection_columns]

        return labels, field_widgets

    @staticmethod
    def __set_widgets_size(labels, field_widgets):
        [label.setFixedSize(125, 25) for label in labels]
        [widget.setFixedSize(225, 25) for widget in field_widgets]

    @staticmethod
    def __add_to_layout(layout_, labels, field_widgets):
        [layout_.addWidget(label, index, 0) for index, label in enumerate(labels)]
        [layout_.addWidget(widget, index, 1) for index, widget in enumerate(field_widgets)]

    def __add_fields(self):

        layout_ = QGridLayout()

        labels, field_widgets = self.__create_qobjects()

        self.__set_widgets_size(labels, field_widgets)

        self.__add_to_layout(layout_, labels, field_widgets)

        self.fields_widget.setLayout(layout_)


class MainWindow(Gui):

    # Stores assigned function buttons
    active_function_buttons: [str]

    def __init__(self, widget_ids, gui_file_path):
        super(MainWindow, self).__init__(widget_ids, gui_file_path) 

        self.show()

        self.db = Database()
        self.event_listener_manager = MainWindowListener(self, self.db)

        self._welcome_window = self.__create_welcome_window()
        self.__show_welcome_window()

        self._edit_database_window = self.__create_edit_db_window()
        self._edit_collection_window = self.__create_edit_collection_window()
        self._create_window = self.__create_create_window()

    def __create_welcome_window(self):
        _widget_ids = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']['WELCOME'])
        _gui_file_path = global_vars['GUI_FILE_PATHS']['WELCOME']

        return WelcomeWindow(_widget_ids, _gui_file_path, self, self.db)

    def __show_welcome_window(self):
        self.setDisabled(True)
        self._welcome_window.show()

    def __create_edit_db_window(self):
        
        _widget_ids = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']['EDIT_DB'])
        _gui_file_path = global_vars['GUI_FILE_PATHS']['EDIT_DB']

        return EditDatabaseWindow(_widget_ids, _gui_file_path, self, self.db)

    def __create_edit_collection_window(self):
        _widget_ids = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']['EDIT_COL'])
        _gui_file_path = global_vars['GUI_FILE_PATHS']['EDIT_COL']

        return EditCollectionWindow(_widget_ids, _gui_file_path, self, self.db)

    def __create_create_window(self):
        _widget_id = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']["CREATE"])
        _gui_file_path = global_vars['GUI_FILE_PATHS']["CREATE"]

        _fields = ["field{}".format(num) for num in range(25)]

        return CreateWindow(_widget_id, _gui_file_path, self, self.db, False, _fields)

    def show_create_window(self):
        self.setDisabled(True)
        self._create_window.show()

    def view_edit_db_window(self):
        self.setDisabled(True)
        self._edit_database_window.show()

    def view_edit_collection_window(self):
        self.setDisabled(True)
        self._edit_collection_window.show()

    def add_function_button_listener(self, button: QPushButton, button_name: str):
        pass


class WelcomeWindow(PopupWindow):
    def __init__(self, widget_ids, gui_file_path, parent_gui, db):
        super(WelcomeWindow, self).__init__(widget_ids, gui_file_path, parent_gui, db)

        self.event_listener_manager = WelcomeWindowListener(self, self.db)


class EditDatabaseWindow(PopupWindow):
    def __init__(self, widget_ids, gui_file_path, parent_gui, db):
        super(EditDatabaseWindow, self).__init__(widget_ids, gui_file_path, parent_gui, db)

        self.event_listener_manager = EditDatabaseWindowListener(self, self.db)


class EditCollectionWindow(PopupWindow):
    def __init__(self, widget_ids, gui_file_path, parent_gui, db):
        super(EditCollectionWindow, self).__init__(widget_ids, gui_file_path, parent_gui, db)

        self.event_listener_manager = EditCollectionWindowListener(self, self.db)


class CreateWindow(DynamicPopupWindow):
    def __init__(self, widget_ids, gui_file_path, parent_gui, db, disable_field_edit=False, fields=[]):
        super().__init__(widget_ids, gui_file_path, parent_gui, db, disable_field_edit=disable_field_edit, fields=fields)

        self._event_listener_manager = CreateWindowListener(self, self.db)
