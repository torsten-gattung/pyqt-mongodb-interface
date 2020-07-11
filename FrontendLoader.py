from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys

from EventListenerManager import EventListenerManager


class Gui(QMainWindow):
    def __init__(self, widget_ids: dict, gui_file_path: str):
        super(Gui, self).__init__()
        uic.loadUi(gui_file_path, self)

        # a dictionary with all widget ids as strings: { QWidgetType: [id1, id2, ..] }
        self.widget_ids: dict = widget_ids

        # Stores all loaded widgets for easy access throughout program
        self.widget_objects = {}

        self.__load_everything()

    def __load_buttons(self):
        for widget in self.widget_ids['QPushButton']:
            self.widget_objects[widget] = self.findChild(QPushButton, widget)

        print("Loaded QPushButton Widgets")

    def __load_labels(self):
        for widget in self.widget_ids['QLabel']:
            self.widget_objects[widget] = self.findChild(QLabel, widget)

        print("Loaded QLabel Widgets")

    def __load_table(self):
        for widget in self.widget_ids['QTableWidget']:
            self.widget_objects[widget] = self.findChild(QTableWidget, widget)

        print("Loaded QTableWidget Widgets")

    def __load_text_edits(self):
        for widget in self.widget_ids['QTextEdit']:
            self.widget_objects[widget] = self.findChild(QTextEdit, widget)

        print("Loaded QTextEdit Widgets")

    def __load_combo_boxes(self):
        for widget in self.widget_ids['QComboBox']:
            self.widget_objects[widget] = self.findChild(QComboBox, widget)

        print("Loaded QComboBox Widgets")

    def __load_everything(self):
        self.__load_buttons()
        self.__load_labels()
        self.__load_table()
        self.__load_text_edits()
        self.__load_combo_boxes()


def start_program(widget_ids: dict, gui_file_path: str):
    app = QApplication(sys.argv)
    window = Gui(widget_ids, gui_file_path)

    EventListenerManager(window.widget_objects)

    window.show()
    app.exec_()
