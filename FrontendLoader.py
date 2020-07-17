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


class MainWindow(Gui):

    # Stores any function button with which has been assigned a custom operation
    active_function_buttons: [str]

    def __init__(self, widget_ids, gui_file_path):
        super(MainWindow, self).__init__(widget_ids, gui_file_path) 

        self.show()

        self.db = Database()
        self.event_listener_manager = MainWindowListener(self, self.db)

        self._edit_database_window = self.__create_edit_db_window()
        self._edit_collection_window = self.__create_edit_collection_window()

        self.welcome_window = self.__create_welcome_window().show()


    def __create_welcome_window(self):
        _widget_ids = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']['WELCOME'])
        _gui_file_path = global_vars['GUI_FILE_PATHS']['WELCOME']

        return PopupWindow(_widget_ids, _gui_file_path, self, self.db)

    def __create_edit_db_window(self):
        
        _widget_ids = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']['EDIT_DB'])
        _gui_file_path = global_vars['GUI_FILE_PATHS']['EDIT_DB']

        return PopupWindow(_widget_ids, _gui_file_path, self, self.db)

    def __create_edit_collection_window(self):
        _widget_ids = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']['EDIT_COL'])
        _gui_file_path = global_vars['GUI_FILE_PATHS']['EDIT_COL']

        return PopupWindow(_widget_ids, _gui_file_path, self, self.db)

    def view_edit_db_window(self):
        self.setDisabled(True)
        self._edit_database_window.show()

    def view_edit_collection_window(self):
        self.setDisabled(True)
        self._edit_collection_window.show()

    def add_function_button_listener(self, button: QPushButton, button_name: str):
        pass

class PopupWindow(Gui):
    def __init__(self, widget_ids, gui_file_path, parent_gui, db):
        super(PopupWindow, self).__init__(widget_ids, gui_file_path)
        self.parent_gui = parent_gui
        self.db = db

        self.event_listener_manager = PopupWindowListener(self, self.db)

    
    def closeEvent(self, a0):
        self.parent_gui.setDisabled(False)  # return 'focus' to parent
        self.hide()
        return super().closeEvent(a0)
