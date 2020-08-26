from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import toolbox as util
from Events import *


global_vars = util.json_to_dict("GLOBAL_VARIABLES.json")


# region Base Classes

class Gui(QMainWindow):

    # Stores all loaded widgets for easy access throughout program
    widget_objects = {}

    def __init__(self, db, widget_ids: dict, gui_file_path: str):
        super().__init__()

        self.db = db
        uic.loadUi(gui_file_path, self)

        self.gui_file_path = gui_file_path

        # holds all widget ids as strings: { QWidgetType: [id1, id2, ..] }
        self.widget_ids: dict = widget_ids

        self._load_all_qt_objects()

    def _load_all_qt_objects(self):
        print("\nLoading all GUI elements...")
        for object_type, id_list in self.widget_ids.items():
            for object_id in id_list:
                exec(
                    "self.widget_objects[object_id] = self.findChild(" + object_type + ", object_id)")

        print("Successfully loaded all GUI elements")


class MainWindow(Gui):

    # Stores assigned function buttons
    active_function_buttons: [str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener = MainWindowListener(self, self.db)

        self._create_sub_windows()

        self.status_bar = self._get_status_bar()

        self.function_windows = dict(self._create_function_windows())

        self.set_status_bar_text()

        # Show at the end because it makes me feel better
        self.show()

    def _create_sub_windows(self):

        self._edit_database_window = self._create_edit_db_window()
        self._edit_collection_window = self._create_edit_collection_window()

        self._create_window = self._make_create_window()
        self._modify_window = self._make_modify_window()
        self._filter_window = self._make_filter_window()
        self._delete_window = self._make_delete_window()

    # region subwindows

    def _create_edit_db_window(self):

        _widget_ids = util.json_to_dict(global_vars['WIDGET_ID']['EDIT_DB'])
        _gui_file_path = global_vars['GUI']['EDIT_DB']

        return EditDatabaseWindow(self, self.db, _widget_ids, _gui_file_path)

    def _create_edit_collection_window(self):
        _widget_ids = util.json_to_dict(global_vars['WIDGET_ID']['EDIT_COL'])
        _gui_file_path = global_vars['GUI']['EDIT_COL']

        return EditCollectionWindow(self, self.db, _widget_ids, _gui_file_path)

    # region CRUD windows

    def _make_create_window(self):
        _widget_id = util.json_to_dict(global_vars['WIDGET_ID']["CREATE"])
        _gui_file_path = global_vars['GUI']["CREATE"]

        _fields = ["field{}".format(num) for num in range(25)]

        return CreateWindow(False, _fields, self, self.db, _widget_id, _gui_file_path)

    def _make_modify_window(self):
        _widget_id = util.json_to_dict(global_vars['WIDGET_ID']["MODIFY"])
        _gui_file_path = global_vars['GUI']["MODIFY"]

        _fields = ["field{}".format(num) for num in range(25)]

        return ModifyWindow(False, _fields, self, self.db, _widget_id, _gui_file_path)

    def _make_filter_window(self):
        _widget_id = util.json_to_dict(global_vars['WIDGET_ID']["FILTER"])
        _gui_file_path = global_vars['GUI']["FILTER"]

        _fields = ["field{}".format(num) for num in range(25)]

        return FilterWindow(False, _fields, self, self.db, _widget_id, _gui_file_path)

    def _make_delete_window(self):
        _widget_id = util.json_to_dict(global_vars['WIDGET_ID']["DELETE"])
        _gui_file_path = global_vars['GUI']["DELETE"]

        _fields = ["field{}".format(num) for num in range(25)]

        return DeleteWindow(False, _fields, self, self.db, _widget_id, _gui_file_path)

    def show_create_window(self):
        self.setDisabled(True)
        self._create_window.show()

    def show_modify_window(self):
        self.setDisabled(True)
        self._modify_window.show()

    def show_filter_window(self):
        self.setDisabled(True)
        self._filter_window.show()

    def show_delete_window(self):
        self.setDisabled(True)
        self._delete_window.show()

    # endregion CRUD windows

    # region Fuction Buttons

    def _function_buttons(self):
        for widget_id, widget in self.widget_objects.items():
            # this RegEx catches all objects with id like "functionNumberButton"
            if re.match("^function.*Button$", widget_id):
                yield widget_id, widget

    def _create_function_windows(self):

        widget_ids = util.json_to_dict(
            global_vars['WIDGET_ID']['FUNCTION_BLANK'])
        filepath = global_vars['GUI']['FUNCTION_BLANK']

        # TODO: find better solution to RuntimeError: dict changed size during iteration
        fnc_buttons = list(self._function_buttons())

        for name, widget in fnc_buttons:
            yield name, FunctionWindow(name, self, self.db, widget_ids, filepath)

    def show_function_window(self, button_name, button):
        # TODO: remove button parameter
        self.function_windows[button_name].show()

    # endregion Function Buttons

    def _get_status_bar(self):
        return self.widget_objects['statusBarConnectionLabel']

    def show_edit_db_window(self):
        self.setDisabled(True)
        self._edit_database_window.show()

    def show_edit_collection_window(self):
        self.setDisabled(True)
        self._edit_collection_window.show()

    # endregion subwindows

    def set_status_bar_text(self):
        text = f"Connected to Mongo Server on //{self.db.host}:{self.db.port}. Nice!"

        self.widget_objects['statusBarCurrentStatusLabel'].setText("Connected")
        self.status_bar.setText(text)


class PopupWindow(Gui):
    def __init__(self, parent_gui, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_gui = parent_gui

    def closeEvent(self, a0):
        self.parent_gui.setDisabled(False)  # return 'focus' to parent
        self.hide()
        return super().closeEvent(a0)


class DynamicPopupWindow(PopupWindow):
    def __init__(self, disable_field_edit=False, fields=[], *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.collection_columns: [str] = self.db.current_collection_columns
        self.collection_columns = fields

        self.fields_widget: QWidget = self.widget_objects['fieldsWidget']
        self.__add_fields()

        self.event_listener_manager = DynamicPopupWindowListener(self, self.db)

    def _create_qobjects(self):
        labels = [QLabel(col_name) for col_name in self.collection_columns]
        field_widgets = [QLineEdit() for _ in self.collection_columns]

        return labels, field_widgets

    @staticmethod
    def _set_widgets_size(labels, field_widgets):
        [label.setFixedSize(125, 25) for label in labels]
        [widget.setFixedSize(225, 25) for widget in field_widgets]

    @staticmethod
    def _add_to_layout(layout_, labels, field_widgets):
        [layout_.addWidget(label, index, 0)
         for index, label in enumerate(labels)]
        [layout_.addWidget(widget, index, 1)
         for index, widget in enumerate(field_widgets)]

    def __add_fields(self):

        layout_ = QGridLayout()

        labels, field_widgets = self._create_qobjects()

        self._set_widgets_size(labels, field_widgets)

        self._add_to_layout(layout_, labels, field_widgets)

        self.fields_widget.setLayout(layout_)


# endregion Base Classes


class WelcomeWindow(Gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener_handler = WelcomeWindowListener(self, self.db)

    def set_main_window_method(self, method):
        self.make_main_window = method

    def create_main_window(self):
        self.make_main_window(self.db)

    def start_program(self):

        self.create_main_window()

        self.close()
        del self

# region Edit DB / Collection Buttons


class EditDatabaseWindow(PopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener_manager = EditDatabaseWindowListener(self, self.db)


class EditCollectionWindow(PopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener_manager = EditCollectionWindowListener(
            self, self.db)


# endregion Edit DB / Collcetion Buttons


# region CRUD Buttons

class CreateWindow(DynamicPopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener_manager = CreateWindowListener(self, self.db)


class FilterWindow(DynamicPopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener_manager = FilterWindowListener(self, self.db)


class ModifyWindow(DynamicPopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener_manager = ModifyWindowListener(self, self.db)


class DeleteWindow(DynamicPopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener_manager = DeleteWindowListener(self, self.db)

# endregion CRUD Buttons


# region Function Buttons

class FunctionWindow(PopupWindow):
    def __init__(self, window_title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(window_title)

# endregion Function Buttons
