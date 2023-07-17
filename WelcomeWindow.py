from Frontend import *
from MainWindow import MainWindow


class WelcomeWindow(Frontend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_main_window = None
        self.event_listener_handler = WelcomeWindowListener(self, self.db)

    def create_main_window(self):
        my_widget_ids: dict = util.json_to_dict(global_vars['WIDGET_ID']['MAIN'])
        gui_file_path = global_vars['GUI']['MAIN']
        MainWindow(self.db, my_widget_ids, gui_file_path)

    def start_program(self):
        self.create_main_window()
        self.close()
        del self
