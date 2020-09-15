from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import toolbox as util
from Events import *


global_vars = util.json_to_dict("GLOBAL_VARIABLES.json")


# region Base Classes

class Gui(QMainWindow):

    def __init__(self, db, widget_ids: dict, gui_file_path: str):
        super().__init__()
        
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


class MainWindow(Gui):

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

    def _format_collection_name(self, col_name):
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

        except AttributeError as e:
            text = "Select a database clicking the 'Database' button"
            self.information_label.setText(text)

            return

        # If no collection selected yet
        try:
            current_collection = self.db.current_collection.name

            current_collection = self._format_collection_name(
                current_collection)

        except AttributeError as e:
            text = f"Selected {current_db} database. Choose a collection by clicking the 'Collection' button"
            self.information_label.setText(text)

            return

        text = f"Loaded {current_collection} collection from {current_db} database"

        self.information_label.setText(text)


class PopupWindow(Gui):
    def __init__(self, parent_gui, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_gui = parent_gui

        # Bring new window to front
        self.raise_()

    def show(self):
        self.parent_gui.setDisabled(True)
        return super().show()

    def closeEvent(self, a0):
        self.parent_gui.setDisabled(False)  # return 'focus' to parent
        self.hide()
        return super().closeEvent(a0)


class DynamicPopupWindow(PopupWindow):
    def __init__(self, disable_field_edit=False, fields=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.first_time = True

        self.label_values = []
        self.field_values = []

        self.labels = {}
        self.fields = {}

        self.fields_container = self.get_fields_container()

        self.event_listener_manager = DynamicPopupWindowListener(self, self.db)

    def get_fields_container(self):
        return self.widget_objects['fieldsWidget']

    def _make_widgets(self):
        label_widgets = [QLabel(col_name) for col_name in self.label_values]
        field_widgets = [QLineEdit() for _ in self.label_values]

        labels = {str(widget_text): widget for widget_text, widget in zip(self.label_values, label_widgets)}
        fields = {str(widget_text): widget for widget_text, widget in zip(self.label_values, field_widgets)}

        return labels, fields

    def _set_widgets_size(self):
        [label.setFixedSize(125, 25) for label in self.labels.values()]
        [field.setFixedSize(225, 25) for field in self.fields.values()]

    def _set_widgets_text(self):
        [label.setText(str(text)) for label, text in zip(self.labels.values(), self.label_values)]
        [field.setText(str(text)) for field, text in zip(self.fields.values(), self.field_values)]

    def label_widgets(self):
        """
        generator that yields a row number and label widget for all labels
        """
        for index, label in enumerate(self.labels.values()):
            yield index, label

    def field_widgets(self):
        """
        generator that yields a row number and field widget for all fields
        """
        for index, field in enumerate(self.fields.values()):
            yield index, field

    def _add_widgets_to_layout(self):
        [self.fields_container_layout.addWidget(label, index, 0) for index, label in self.label_widgets()]
        [self.fields_container_layout.addWidget(field, index, 1) for index, field in self.field_widgets()]

    def clear_layout(self):
        while not self.fields_container_layout.isEmpty():
            # According to some guy on the internet, this stops memory leaks
            # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt/13103617
            self.fields_container_layout.itemAt(0).widget().deleteLater()
            self.fields_container_layout.itemAt(0).widget().setParent(None)

    def _set_fields(self):

        # FIXME: layout must be only be set the first time this method is called
        # Add a flag to determine whether this is the first time
        if self.first_time:
            self.first_time = False
            self.fields_container_layout = QGridLayout(self.fields_container)

        else:
            self.clear_layout()

        self.labels, self.fields = self._make_widgets()

        self._set_widgets_size()
        self._add_widgets_to_layout()
        self._set_widgets_text()

        self.fields_container.setLayout(self.fields_container_layout)

    def remove_all(self):
        """
        removes all fields and labels from layout
        """

    def check_current_collection(self):
        if self.db.current_collection is None:
            raise CollectionNotChosenYetException()

    def _get_label_and_field_values(self):
        
        template = self.db.current_collection.get_field_template()

        label_values = template.keys()
        field_values= template.values()

        print("Got field and label values!")

        for label, field in zip(label_values, field_values):
            print(f"{label}: {field}")

        return label_values, field_values
    
    def set_fields(self):
        self.check_current_collection()

        self.label_values, self.field_values = self._get_label_and_field_values()

        self._set_fields()

    def disable_field(self, field_name):
        self.fields[field_name].setDisabled(True)

    def show(self):
        try:
            self.set_fields()
            return super().show()
            
        except CollectionNotChosenYetException as e:
            # TODO: Show popup window to tell user to choose database and collection first
            self.msg = PopupTextmessage(self, text="Must choose Database and Collection First")
            print("Cannot open CRUD window without choosing a collection first")
            return


class PopupTextmessage(PopupWindow):
    def __init__(self, parent, text="Warning"):

        ids = util.json_to_dict(global_vars['WIDGET_ID']['POPUP_TEXTMESSAGE'])
        path_ = global_vars['GUI']['POPUP_TEXTMESSAGE']

        super().__init__(parent_gui=parent,
                         widget_ids=ids,
                         gui_file_path=path_,
                         db=None
                        )

        self.setMessage(text)

        self.setOkayButtonListener()

        self.show()

    def setMessage(self, text):
        self.widget_objects['message'].setText(text)

    def findOkayButton(self):
        return self.widget_objects['okayButton']

    def setOkayButtonListener(self):
        okayButton = self.findOkayButton()
        okayButton.clicked.connect(self.okayButtonOnClick)

    def okayButtonOnClick(self):
        self.close()

    def closeEvent(self, a0):
        return super().closeEvent(a0)


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


class DatabaseWindow(PopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener = DatabaseWindowListener(self, self.db)

        self.db_list = self._get_database_list()
        self.populate_database_list()

        self.current_db_label = None
        self.local_col_count_label = None
        self.local_doc_count_label = None
        self.database_count_label = None

        self._assign_information_labels()
        self.update_information_labels(with_default=True)

    def _assign_information_labels(self):
        self.current_db_label = self.widget_objects['currentDatabaseLabel']
        self.local_col_count_label = self.widget_objects['collectionCountLabel']
        self.local_doc_count_label = self.widget_objects['localDocumentCountLabel']
        self.database_count_label = self.widget_objects['databaseCountLabel']

    def _get_database_list(self):
        return self.widget_objects['databaseList']

    def update_collection_list(self):
        self.parent_gui.update_collection_list()

    def populate_database_list(self):
        self.db_list.addItems(self.db.db_names)

    def get_selected_database(self):
        selected_db = ""

        try:
            selected_db = self.db_list.selectedItems()[0].text()

            return selected_db
        except IndexError as e:
            # TODO: add popup warning here
            print("Must Select a database first!")

            return

    def _update_current_database_label(self, with_default):
        if with_default:
            self.current_db_label.setText("N/A")

        else:
            self.current_db_label.setText(self.db.current_db.name)

    def _update_local_collection_count(self, with_default):
        if with_default:
            self.local_col_count_label.setText("N/A")

        else:
            count_ = len(self.db.current_db.list_collection_names())
            count_ = str(count_)
            self.local_col_count_label.setText(count_)
    
    def _update_local_doc_count(self, with_default):
        if with_default:
            self.local_doc_count_label.setText("N/A")

        else:
            count_ = str(self.db.get_current_db_doc_count())
            self.local_doc_count_label.setText(count_)

    def _update_local_db_count(self, with_default):
        if with_default:
            self.database_count_label.setText("N/A")

        else:
            count_ = len(self.db.db_dict.keys())
            count_ = str(count_)
            self.database_count_label.setText(count_)

    def update_information_labels(self, with_default=False):

        # TODO: update information labels for Database Window

        self._update_current_database_label(with_default)
        self._update_local_collection_count(with_default)
        self._update_local_doc_count(with_default)
        self._update_local_db_count(with_default)

        if not with_default:
            self.parent_gui.update_information_labels()


class CollectionWindow(PopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener = CollectionWindowListener(self, self.db)

        self.collection_list = self._get_collection_list_widget()

        self.current_col_label = None
        self.current_db_label = None
        self.doc_count_label = None
        self.avg_doc_size_label = None
        self.col_size = None

        self.assign_information_labels()
        self.update_information_labels(with_default=True)

    def assign_information_labels(self):
        self.current_col_label = self.widget_objects['currentCollectionLabel']
        self.current_db_label = self.widget_objects['currentDatabaseLabel']
        self.db_count_label = self.widget_objects['databaseCountLabel']
        self.doc_count_label = self.widget_objects['documentCountLabel']

    def _get_collection_list_widget(self):
        return self.widget_objects['collectionList']

    def clear_collection_list(self):
        while len(self.collection_list) > 0:
            self.collection_list.takeItem(0)

    def update_collection_list(self):
        self.clear_collection_list()
        self.populate_collection_list()

    def populate_collection_list(self):
        names = self._get_collection_names()
        self.collection_list.addItems(names)

    def _get_collection_names(self):
        selected_db = self.db.current_db

        return selected_db.list_collection_names()

    def get_selected_collection(self):
        try:
            selected_collection = self.collection_list.selectedItems()[0].text()
            return selected_collection

        except IndexError as e:
            print("Must select a collection first!")
            return

    def _update_current_col_label(self, with_default):
        if with_default:
            self.current_col_label.setText("N/A")

        else:
            self.current_col_label.setText(self.db.current_collection.name)

    def _update_current_db_label(self, with_default):
        if with_default:
            self.current_db_label.setText("N/A")

        else:
            self.current_db_label.setText(self.db.current_db.name)

    def _update_db_count_label(self, with_default):
        if with_default:
            self.db_count_label.setText("N/A")

        else:
            count_ = len(self.db.db_dict.keys())
            count_ = str(count_)
            self.db_count_label.setText(count_)

    def _update_doc_count_label(self, with_default):
        if with_default:
            self.doc_count_label.setText("N/A")

        else:
            count_ = self.db.current_collection.count_documents({})
            count_ = str(count_)

            self.doc_count_label.setText(count_)

    def update_information_labels(self, with_default=False):

        self._update_current_col_label(with_default)
        self._update_current_db_label(with_default)
        self._update_db_count_label(with_default)
        self._update_doc_count_label(with_default)

        if not with_default:
            self.parent_gui.update_information_labels()

    def show(self):
        if self.db.current_db is None:
            print("Must choose database before you can open the Collection Window")
            self.msg = PopupTextmessage(self, text="Must choose database before you can open the Collection Window")
            return
        else:
            return super().show()


# endregion Edit DB / Collection Buttons

# region CRUD Buttons

class CreateWindow(DynamicPopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = CreateWindowListener(self, self.db)

    def set_fields(self):
        super().set_fields()
        
        self.disable_field('_id')


class FilterWindow(DynamicPopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = FilterWindowListener(self, self.db)

    def set_fields(self):
        super().set_fields()


class ModifyWindow(DynamicPopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = ModifyWindowListener(self, self.db)

    def set_fields(self):
        super().set_fields()

        self.disable_field('_id')


class DeleteWindow(DynamicPopupWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = DeleteWindowListener(self, self.db)

    def set_fields(self):
        super().set_fields()

        self.disable_field('_id')

# endregion CRUD Buttons


# region Function Buttons

class FunctionWindow(PopupWindow):
    def __init__(self, window_title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(window_title)

# endregion Function Buttons
