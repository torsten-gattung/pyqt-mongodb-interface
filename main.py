from FrontendLoader import *
from EventListenerManager import EventListenerManager, MainWindowEventListenerManager
from Database import Database
import utility as util



global_vars: dict = util.load_json_file_as_dict("GLOBAL_VARIABLES.json")

widget_ids: dict = util.load_json_file_as_dict("WIDGET_ID.json")
mini_gui_widget_ids = util.load_json_file_as_dict("EDIT_DATABASE_WIDGET_ID.json")


def test_popup_screen(widget_ids: dict, gui_file_path: str, event_listener_manager: EventListenerManager):
    app = QApplication(sys.argv)

    main_window = Gui(widget_ids, gui_file_path)

    # EventListenerManager(main_window, db)

    main_window.show()
    app.exec_()


def start_program(widget_ids: dict, gui_file_path: str):
    app = QApplication(sys.argv)

    main_window = MainWindow(widget_ids, gui_file_path)

    db = Database()

    event_listener_manager = MainWindowEventListenerManager(main_window, db)

    main_window.show()
    app.exec_()


if __name__ == "__main__":
    start_program(widget_ids, global_vars['GUI_FILE_PATH'])
