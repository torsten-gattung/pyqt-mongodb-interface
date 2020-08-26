from Frontend import *
from Backend import *
import toolbox as util


global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")
widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['MAIN'])


def launch_welcome_window(db):
    widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['WELCOME'])
    gui_file_path = global_vars['GUI']['WELCOME']
    
    window = WelcomeWindow(db, widget_ids, gui_file_path)

    window.set_main_window_method(launch_main_window)

    window.show()


def launch_main_window(db):

    widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['MAIN'])
    gui_file_path = global_vars['GUI']['MAIN']

    return MainWindow(db, widget_ids, gui_file_path)


def start_program(global_vars=global_vars):
    app = QApplication(sys.argv)

    mongo_handler = MongoHandler()

    launch_welcome_window(mongo_handler)
    
    # main_window = launch_main_window(mongo_handler)

    app.exec_()


if __name__ == "__main__":
    start_program(global_vars)
