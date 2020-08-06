from Frontend import *
import toolbox as util


global_vars: dict = util.json_to_dict("GLOBAL_VARIABLES.json")
widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['MAIN'])


def start_program(global_vars=global_vars):
    app = QApplication(sys.argv)

    _widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['MAIN'])
    _gui_file_path = global_vars['GUI']['MAIN']

    main_window = MainWindow(_widget_ids, _gui_file_path)

    app.exec_()


if __name__ == "__main__":
    start_program(global_vars)
