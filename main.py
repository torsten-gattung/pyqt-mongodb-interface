from Frontend import *
from Backend import *
import toolbox as util
import sys

global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")
widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['MAIN'])


def start_main_window(db):
    widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['MAIN'])
    gui_file_path = global_vars['GUI']['MAIN']
    MainWindow(db, widget_ids, gui_file_path)


def launch_welcome_window(mongodb):
    widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['WELCOME'])
    gui_file_path = global_vars['GUI']['WELCOME']
    welcome_window = WelcomeWindow(mongodb, widget_ids, gui_file_path)
    welcome_window.set_main_window_method(start_main_window)
    welcome_window.show()


def start_program():
    app = QApplication(sys.argv)
    mongo_handler = MongoHandler()
    launch_welcome_window(mongo_handler)
    app.exec_()


if __name__ == "__main__":
    start_program()
