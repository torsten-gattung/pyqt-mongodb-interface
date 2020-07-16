from FrontendLoader import *
from EventListenerManager import EventListenerManager, MainWindowEventListenerManager
from Database import Database
import functions as fn



global_vars: dict = fn.load_json_file_as_dict("GLOBAL_VARIABLES.json")

widget_ids: dict = fn.load_json_file_as_dict("WIDGET_ID.json")
mini_gui_widget_ids = fn.load_json_file_as_dict("EDIT_DATABASE_WIDGET_ID.json")


def test_popup_screen(widget_ids: dict, gui_file_path: str):
    app = QApplication(sys.argv)

    # Gui
    main_window = Gui(widget_ids, gui_file_path)

    # Database
    # db = Database()

    # Event Listener Manager
    # EventListenerManager(main_window, db)

    main_window.show()
    app.exec_()


def start_program(widget_ids: dict, gui_file_path: str):
    app = QApplication(sys.argv)

    # Gui
    main_window = MainWindow(widget_ids, gui_file_path)

    # Database
    db = Database()

    # Event Listener Manager
    MainWindowEventListenerManager(main_window, db)

    main_window.show()
    app.exec_()


test_popup_screen(mini_gui_widget_ids, "edit_database_gui.ui")
start_program(widget_ids, global_vars['GUI_FILE_PATH'])
