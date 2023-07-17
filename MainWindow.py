from Frontend import *
from PopupWindow import *
from CRUDWindow import *
from DatabaseWindow import DatabaseWindow

global_vars = util.json_to_dict("GLOBAL_VARIABLES.json")


class MainWindow(Frontend):
    # Stores assigned function buttons
    active_function_buttons: [str]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_listener = MainWindowListener(self, self.db)
        self._create_sub_windows()
        self.function_windows = dict(self._create_function_windows())
        self.status_bar = self._get_status_bar()
        self.set_status_bar_text()
        self.update_information_labels()
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
        return DatabaseWindow(self, self.db, _widget_ids, _gui_file_path)

    def _create_edit_collection_window(self):
        _widget_ids = util.json_to_dict(global_vars['WIDGET_ID']['EDIT_COL'])
        _gui_file_path = global_vars['GUI']['EDIT_COL']
        return CollectionWindow(self, self.db, _widget_ids, _gui_file_path)

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
        self._create_window.show()

    def show_modify_window(self):
        self._modify_window.show()

    def show_filter_window(self):
        self._filter_window.show()

    def show_delete_window(self):
        self._delete_window.show()

    # endregion CRUD windows

    # region Function Buttons

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

    def _get_information_label(self):
        return self.widget_objects['loadedFromLabel']

    def show_edit_db_window(self):
        self._edit_database_window.show()

    def show_edit_collection_window(self):
        self._edit_collection_window.show()

    def update_collection_list(self):
        self._edit_collection_window.update_collection_list()

    # endregion subwindows

    def set_status_bar_text(self):
        text = f"Connected to Mongo Server on //{self.db.host}:{self.db.port}"

        self.widget_objects['statusBarCurrentStatusLabel'].setText("Connected")
        self.status_bar.setText(text)

    @staticmethod
    def _format_collection_name(col_name):
        """
        Formats something.col_name into col_name
        """
        name_ = col_name.split('.')
        if len(name_) > 1:
            return ".".join(name_[1:])
        else:
            return col_name

    def update_information_labels(self):
        self.information_label = self._get_information_label()

        current_db = ""
        current_collection = ""
        text = ""

        # If no DB selected yet
        try:
            current_db = self.db.current_db.name
        except AttributeError:
            text = "Select a database clicking the 'Database' button"
            self.information_label.setText(text)
            return

        # If no collection selected yet
        try:
            current_collection = self.db.current_collection.name
            current_collection = self._format_collection_name(current_collection)
        except AttributeError:
            text = f"Selected {current_db} database. Choose a collection by clicking the 'Collection' button"
            self.information_label.setText(text)
            return

        text = f"Loaded {current_collection} collection from {current_db} database"
        self.information_label.setText(text)
