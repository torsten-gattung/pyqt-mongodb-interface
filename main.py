# This software is covered by the MIT License.

# Copyright (c) 2020 Abdulaziz Nal.

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions: The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import functions as fn
from FrontendLoader import *
from EventListenerManager import EventListenerManager, MainWindowEventListenerManager
from Database import Database


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
