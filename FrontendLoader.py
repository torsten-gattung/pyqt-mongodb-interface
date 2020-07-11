from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys


class Gui(QMainWindow):
    def __init__(self, widget_ids:dict, gui_file_path: str):
        super(Gui, self).__init__()
        uic.loadUi(gui_file_path, self)
        
        self.widget_ids = widget_ids    # a dictionary with all widget ids as strings

        self.widget_objects = []    # Stores all loaded widgets for easy access throughout program

        self.__load_everything()

    def __show_all_widget_ids(self):
        [print(button_name) for button_name in self.widget_ids['QPushButton']]
    
    def __load_widget_objects(self, widgetType):
        print("Loading all ids in ", str(widgetType))
        for widget_id in self.widget_ids[widgetType]:
            print(str(widget_id))

    def __load_everything(self):
        for widgetType in self.widget_ids.keys():
            self.__load_widget_objects(widgetType)


def start_program(widget_ids: dict, gui_file_path: str):
    app = QApplication(sys.argv)
    window = Gui(widget_ids, gui_file_path)
    window.show()
    app.exec_()
