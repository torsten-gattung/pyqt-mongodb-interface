from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('static_gui.ui', self)

        self.__load_everything()
        self.__test_load_button()

    def __load_all_buttons(self):
        pass

    def __load_all_labels(self):
        pass

    def __load_all_text_entry_boxes(self):
        pass

    def __load_dropdown_menus(self):
        pass
    
    def __load_everything(self):
        self.__load_all_buttons()
        self.__load_all_labels()
        self.__load_all_text_entry_boxes()
        self.__load_dropdown_menus()

    def __test_load_button(self):
        self.test_button:QObject = self.findChild(QPushButton, 'createButton')
        self.test_button.clicked.connect(self.__say_hi)
        self.test_button

    def __say_hi(self):
        print("Hello World!")


def start_program():
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
