# from Frontend import *
from PyQt5.QtWidgets import QApplication
import Backend
from WelcomeWindow import WelcomeWindow

import toolbox as util
import sys

global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")
widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['MAIN'])


def launch_welcome_window(mongodb):
    my_widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['WELCOME'])
    gui_file_path = global_vars['GUI']['WELCOME']
    welcome_window = WelcomeWindow(mongodb, my_widget_ids, gui_file_path)
    welcome_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launch_welcome_window(Backend.MongoHandler())
    # start_main_window(Backend.MongoHandler())
    app.exec_()
