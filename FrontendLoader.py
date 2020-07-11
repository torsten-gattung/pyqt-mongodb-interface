from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys


class Gui(QMainWindow):
    def __init__(self, widget_ids:dict, gui_file_path: str):
        super(Gui, self).__init__()
        uic.loadUi(gui_file_path, self)
        
        self.widget_ids:dict = widget_ids    # a dictionary with all widget ids as strings: { QWidgetType: [id1, id2, ..] }

        self.widget_objects = []    # Stores all loaded widgets for easy access throughout program

        self.__load_everything(),
        self.__test_click_everything()
    
    def __load_widget_objects(self, widgetType):
        print("Loading all ids in ", str(widgetType))
        for widget_id in self.widget_ids[widgetType]:
            print(str(widget_id))

    def __load_buttons(self):
        for widget in self.widget_ids['QPushButton']:
            self.widget_objects.append(self.findChild(QPushButton, widget))

        print("Loaded QPushButton Widgets")

    def __load_labels(self):
        for widget in self.widget_ids['QLabel']:
            self.widget_objects.append(self.findChild(QPushButton, widget))

        print("Loaded QLabel Widgets")

    def __load_table(self):
        for widget in self.widget_ids['QTableWidget']:
            self.widget_objects.append(self.findChild(QPushButton, widget))

        print("Loaded QTableWidget Widgets")

    def __load_text_edits(self):
        for widget in self.widget_ids['QTextEdit']:
            self.widget_objects.append(self.findChild(QPushButton, widget))

        print("Loaded QTextEdit Widgets")

    def __load_combo_boxes(self):
        for widget in self.widget_ids['QComboBox']:
            self.widget_objects.append(self.findChild(QPushButton, widget))

        print("Loaded QComboBox Widgets")

    def __load_everything(self):
        self.__load_buttons()
        self.__load_labels()
        self.__load_table()
        self.__load_text_edits()
        self.__load_combo_boxes()

    def __say_hi(self):
        print("says hi!")

    def __test_click_everything(self):
        for widget in self.widget_objects:
            try:
                widget.clicked.connect(self.__say_hi)
            except Exception as e: 
                print("something went wrong, ", e)



def start_program(widget_ids: dict, gui_file_path: str):
    app = QApplication(sys.argv)
    window = Gui(widget_ids, gui_file_path)
    window.show()
    app.exec_()
