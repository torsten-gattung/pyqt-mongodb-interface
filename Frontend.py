from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import toolbox as util
from Events import *
from Backend import *


global_vars = util.json_to_dict("GLOBAL_VARIABLES.json")


# region Base Classes

class Gui(QMainWindow):
    
    # Stores all loaded widgets for easy access throughout program
    widget_objects = {}

    def __init__(self, widget_ids: dict, gui_file_path: str):
        super().__init__()
        uic.loadUi(gui_file_path, self)

        self.gui_file_path = gui_file_path

        # holds all widget ids as strings: { QWidgetType: [id1, id2, ..] }
        self.widget_ids: dict = widget_ids

        self.__load_all_qt_objects()

    def __load_all_qt_objects(self):
        print("\nLoading all GUI elements...")
        for object_type, id_list in self.widget_ids.items():
            for object_id in id_list:
                exec("self.widget_objects[object_id] = self.findChild(" + object_type + ", object_id)")

        print("Successfully loaded all GUI elements")


class MainWindow(Gui):
    
    # Stores assigned function buttons
    active_function_buttons: [str]

    def __init__(self, widget_ids, gui_file_path):
        super().__init__(widget_ids, gui_file_path) 

        self.show()

        self.db = MongoHandler()
        self.event_listener_manager = MainWindowListener(self, self.db)

        self._welcome_window = self.__create_welcome_window()
        self.__show_welcome_window()

        self._edit_database_window = self.__create_edit_db_window()
        self._edit_collection_window = self.__create_edit_collection_window()

        self._create_window = self.__create_create_window()
        self._modify_window = self.__create_modify_window()
        self._filter_window = self.__create_filter_window()
        self._delete_window = self.__create_delete_window()

    def __create_welcome_window(self):
        _widget_ids = util.json_to_dict(global_vars['WIDGET_ID']['WELCOME'])
        _gui_file_path = global_vars['GUI']['WELCOME']

        return WelcomeWindow(self, self.db, _widget_ids, _gui_file_path)

    def __show_welcome_window(self):
        self.setDisabled(True)
        self._welcome_window.show()

    def __create_edit_db_window(self):
        
        _widget_ids = util.json_to_dict(global_vars['WIDGET_ID']['EDIT_DB'])
        _gui_file_path = global_vars['GUI']['EDIT_DB']

        return EditDatabaseWindow(self, self.db, _widget_ids, _gui_file_path)

    def __create_edit_collection_window(self):
        _widget_ids = util.json_to_dict(global_vars['WIDGET_ID']['EDIT_COL'])
        _gui_file_path = global_vars['GUI']['EDIT_COL']

        return EditCollectionWindow(self, self.db, _widget_ids, _gui_file_path)

    # region CRUD windows

    def __create_create_window(self):
        _widget_id = util.json_to_dict(global_vars['WIDGET_ID']["CREATE"])
        _gui_file_path = global_vars['GUI']["CREATE"]

        _fields = ["field{}".format(num) for num in range(25)]

        return CreateWindow(False, _fields, self, self.db, _widget_id, _gui_file_path)

    def __create_modify_window(self):
        _widget_id = util.json_to_dict(global_vars['WIDGET_ID']["MODIFY"])
        _gui_file_path = global_vars['GUI']["MODIFY"]

        _fields = ["field{}".format(num) for num in range(25)]

        return ModifyWindow(False, _fields, self, self.db, _widget_id, _gui_file_path)

    def __create_filter_window(self):
        _widget_id = util.json_to_dict(global_vars['WIDGET_ID']["FILTER"])
        _gui_file_path = global_vars['GUI']["FILTER"]

        _fields = ["field{}".format(num) for num in range(25)]

        return FilterWindow(False, _fields, self, self.db, _widget_id, _gui_file_path)

    def __create_delete_window(self):
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

    def view_edit_db_window(self):
        self.setDisabled(True)
        self._edit_database_window.show()

    def view_edit_collection_window(self):
        self.setDisabled(True)
        self._edit_collection_window.show()

    def add_function_button_listener(self, button: QPushButton, button_name: str):
        pass


class PopupWindow(Gui):
    def __init__(self, parent_gui, db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_gui = parent_gui
        self.db = db

    
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

    def __create_qobjects(self):
        labels = [QLabel(col_name) for col_name in self.collection_columns]
        field_widgets = [QLineEdit() for _ in self.collection_columns]

        return labels, field_widgets

    @staticmethod
    def __set_widgets_size(labels, field_widgets):
        [label.setFixedSize(125, 25) for label in labels]
        [widget.setFixedSize(225, 25) for widget in field_widgets]

    @staticmethod
    def __add_to_layout(layout_, labels, field_widgets):
        [layout_.addWidget(label, index, 0) for index, label in enumerate(labels)]
        [layout_.addWidget(widget, index, 1) for index, widget in enumerate(field_widgets)]

    def __add_fields(self):

        layout_ = QGridLayout()

        labels, field_widgets = self.__create_qobjects()

        self.__set_widgets_size(labels, field_widgets)

        self.__add_to_layout(layout_, labels, field_widgets)

        self.fields_widget.setLayout(layout_)


# endregion Base Classes


class WelcomeWindow(PopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener_manager = WelcomeWindowListener(self, self.db)


# region Edit DB / Collection Buttons


class EditDatabaseWindow(PopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener_manager = EditDatabaseWindowListener(self, self.db)


class EditCollectionWindow(PopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener_manager = EditCollectionWindowListener(self, self.db)


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

#endregion CRUD Buttons
