from PyQt5 import uic

from Events import *
import toolbox as util

global_vars = util.json_to_dict("GLOBAL_VARIABLES.json")

# region Base Classes


class Frontend(QMainWindow):
    def __init__(self, db, widget_ids: dict, gui_file_path: str):
        super().__init__(None)

        # Stores all loaded widgets for easy access
        self.widget_objects = {}

        self.db = db
        uic.loadUi(gui_file_path, self)

        self.gui_file_path = gui_file_path

        # holds all widget ids as strings: { QWidgetType: [id1, id2, ..] }
        self.widget_ids: dict = widget_ids

        self._load_all_qt_objects()

    def _load_all_qt_objects(self):
        for object_type, id_list in self.widget_ids.items():
            for object_id in id_list:
                exec(
                    "self.widget_objects[object_id] = self.findChild(" + object_type + ", object_id)")


# region Edit DB / Collection Buttons
