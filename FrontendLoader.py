from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys

class Gui(QMainWindow):

    # Stores all loaded widgets for easy access throughout program
    widget_objects = {}

    def __init__(self, widget_ids: dict, gui_file_path: str):
        super(Gui, self).__init__()
        uic.loadUi(gui_file_path, self)

        # a dictionary with all widget ids as strings: { QWidgetType: [id1, id2, ..] }
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


    def add_function_button_listener(self, button: QPushButton, button_name: str):
        pass
