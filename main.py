from FrontendLoader import *
import utility as util


global_vars: dict = util.load_json_file_as_dict("GLOBAL_VARIABLES.json")
widget_ids: dict = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']['MAIN'])


def start_program(global_vars=global_vars):
    app = QApplication(sys.argv)

    _widget_ids: dict = util.load_json_file_as_dict(global_vars['WIDGET_ID_FILE_PATHS']['MAIN'])
    _gui_file_path = global_vars['GUI_FILE_PATHS']['MAIN']

    main_window = MainWindow(_widget_ids, _gui_file_path)

    app.exec_()


if __name__ == "__main__":
    start_program(global_vars)
