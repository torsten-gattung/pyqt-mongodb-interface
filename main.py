from FrontendLoader import *
import utility as util


global_vars: dict = util.load_json_file_as_dict("GLOBAL_VARIABLES.json")
widget_ids: dict = util.load_json_file_as_dict("WIDGET_ID.json")


def start_program(widget_ids: dict, gui_file_path: str):
    app = QApplication(sys.argv)

    main_window = MainWindow(widget_ids, gui_file_path)

    main_window.show()
    app.exec_()


if __name__ == "__main__":
    start_program(widget_ids, global_vars['GUI_FILE_PATH'])
