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


class PopupConfirmBox(PopupWindow):
    def __init__(self, parent, text="Warning", callback=None):
    
        ids = util.json_to_dict(global_vars['WIDGET_ID']['POPUP_CONFIRM'])
        path_ = global_vars['GUI']['POPUP_CONFIRM']

        super().__init__(parent_gui=parent,
                         widget_ids=ids,
                         gui_file_path=path_,
                         db=None
                        )

        self.callback = callback

        self.confirm_button = self._get_confirm_button()
        self.cancel_button = self._get_cancel_button()

        self.set_button_listeners()

        self.setMessage(text)

        self.show()


    def _get_confirm_button(self):
        return self.widget_objects['confirmButton']

    def _get_cancel_button(self):
        return self.widget_objects['cancelButton']


    def set_button_listeners(self):
        self.confirm_button.clicked.connect(self.confirm_button_onclick)        
        self.cancel_button.clicked.connect(self.cancel_button_onclick)


    def confirm_button_onclick(self):
        self.close()
        return self.callback()

    def cancel_button_onclick(self):
        self.close()
        return


    def setMessage(self, text):
        self.widget_objects['message'].setText(text)


class CRUDWindow(PopupWindow):
    def __init__(self, disable_field_edit=False, fields=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.first_time = True

        self.label_values = []
        self.field_values = []

        self.labels = {}
        self.fields = {}

        self.fields_container = self.get_fields_container()


    def get_fields_container(self):
        return self.widget_objects['fieldsWidget']


    def _set_widgets_size(self):
        [label.setFixedSize(125, 25) for label in self.labels.values()]
        [field.setFixedSize(225, 25) for field in self.fields.values()]

    def _set_widgets_text(self):
        [label.setText(str(text)) for label, text in zip(self.labels.values(), self.label_values)]
        [field.setText(str(text)) for field, text in zip(self.fields.values(), self.field_values)]

    def _label_widgets(self):
        """
        generator that yields a row number and label widget for all labels
        """
        for index, label in enumerate(self.labels.values()):
            yield index, label

    def _field_widgets(self):
        """
        generator that yields a row number and field widget for all fields
        """
        for index, field in enumerate(self.fields.values()):
            yield index, field

    def _add_widgets_to_layout(self):
        [self.fields_container_layout.addWidget(label, index, 0) for index, label in self._label_widgets()]
        [self.fields_container_layout.addWidget(field, index, 1) for index, field in self._field_widgets()]

    def clear_layout(self):
        while not self.fields_container_layout.isEmpty():
            # According to some guy on the internet, this stops memory leaks
            # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt/13103617
            self.fields_container_layout.itemAt(0).widget().deleteLater()
            self.fields_container_layout.itemAt(0).widget().setParent(None)

    def _make_widgets(self):
        label_widgets = [QLabel(col_name) for col_name in self.label_values]
        field_widgets = [QLineEdit() for _ in self.label_values]

        paired_label_values = {str(widget_text): widget for widget_text, widget in zip(self.label_values, label_widgets)}
        paired_field_values = {str(widget_text): widget for widget_text, widget in zip(self.label_values, field_widgets)}

        return paired_label_values, paired_field_values

    def _setup_layout(self):
        if self.first_time:
            self.first_time = False
            self.fields_container_layout = QGridLayout(self.fields_container)

        else:
            self.clear_layout()

    def show_empty_label(self):
        empty_label = QLabel("This collection is empty")
        self.fields_container_layout.addWidget(empty_label, 0, 0)

    def _set_fields(self, empty_collection=False):
    
        self._setup_layout()

        if empty_collection:
            self.show_empty_label()
        
        else:

            self.labels, self.fields = self._make_widgets()

            self._set_widgets_size()
            self._add_widgets_to_layout()

        self.fields_container.setLayout(self.fields_container_layout)

    def _check_current_collection(self):
        if self.db.current_collection is None:
            raise CollectionNotChosenYetException()

    def _get_label_and_field_values(self):
        template = self.db.current_collection.get_field_template()
    
        label_values = template.keys()
        field_values= template.values()

        return label_values, field_values


    def set_fields(self):
        self._check_current_collection()

        try:
            self.label_values, self.field_values = self._get_label_and_field_values()
            self._set_fields()
        
        except EmptyCollectionException as e:
            self._set_fields(empty_collection=True)


    def disable_id_field(self):
        try:
            self.disable_field('_id')
        
        except KeyError as e:
            # Likely empty collection
            pass

        except RuntimeError as r:
            # This happens because '_id' key is present but referenced object is deleted
            pass


    def disable_field(self, field_name):
        """
        Makes a field unable to have its value modified
        """
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


    def update_collection_list(self):
        self.parent_gui.update_collection_list()


    def _get_database_list(self):
        return self.widget_objects['databaseList']

    def empty_db_list(self):
        
        for _ in range(self.db_list.count()):
            self.db_list.takeItem(0)

    def populate_database_list(self):
        self.db_list.addItems(self.db.db_names)

    def update_database_list(self):

        # Always empty list first
        self.empty_db_list()

        self.populate_database_list()


    def get_selected_database(self):
        selected_db = ""

        try:
            selected_db = self.db_list.selectedItems()[0].text()

            return selected_db
        except IndexError as e:

            msg = "Must select a database first"

            raise DatabaseNotSelectedException(msg)


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

        self._update_current_database_label(with_default)
        self._update_local_collection_count(with_default)
        self._update_local_doc_count(with_default)
        self._update_local_db_count(with_default)

        if not with_default:
            self.parent_gui.update_information_labels()


    def switch_to_selected_database(self):
        try:
            selected_db = self.get_selected_database()

            self.db.switch_db(selected_db)
            self.update_collection_list()
            self.update_information_labels()

            self.close()

        except DatabaseNotSelectedException:
            msg = "Must Choose Database First"
            self.msg = PopupTextmessage(self, text=msg)

    def create_new_database(self):

        # TODO: add validation for database names

        db_name_input = self.widget_objects['databaseNameInput']
        # selected_template = self.widget_objects['templateList'].selectedItems()[0]

        database_name = db_name_input.text()
        # database_template = selected_template.text()

        self.db.create_new_database(db_name=database_name, template=None)

        self.update_database_list()
        self.msg = PopupTextmessage(self, f"Created Database: {database_name}")


    def delete_selected_database(self):

        # BUG #7: Database will not be deleted unless highlighted in list before

        try:
            selected_db = self.get_selected_database()
            self.db.drop_selected_database(db_name=selected_db)

            self.update_database_list()
            self.update_information_labels(with_default=True)

            self.msg = PopupTextmessage(self, f"Dropped {selected_db}")

        except DatabaseNotSelectedException:
            self.msg = PopupTextmessage(self, "Must Select database first")
            

    def showEvent(self, a0):
        self.update_database_list()
        super().showEvent(a0)


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
            raise CollectionNotChosenYetException("Must select a collection first")
            return

    def switch_to_selected_collection(self):
        try:
            selected_collection = self.get_selected_collection()

            self.db.switch_collection(selected_collection)

            self.update_information_labels()

            self.close()

        except CollectionNotChosenYetException:
            self.msg = PopupTextmessage(self, "Must select a collection first")


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


    def get_changed_collection_name_field(self):
        return self.widget_objects['collectionNameLineEdit']

    def get_changed_collection_name(self):
        collection_name = self.get_changed_collection_name_field().text()

        if len(collection_name) == 0:
            raise BadFieldValueException("No collection name was provided")

        else:
            return collection_name

    def change_collection_name(self):
        try:
            selected_collection = self.get_selected_collection()
            new_collection_name = self.get_changed_collection_name()

            self.db.change_collection_name(selected_collection, new_collection_name)

            self.update_collection_list()
            self.update_information_labels(with_default=True)

        except CollectionNotChosenYetException:
            self.msg = PopupTextmessage(self, "Must select a collection first")
        
        except BadFieldValueException:
            self.msg = PopupTextmessage(self, "Must provide a new name for collection")


    def get_new_collection_name_field(self):
        return self.widget_objects['newCollectionNameLineEdit']

    def get_new_collection_name(self):
        new_collection_name = self.get_new_collection_name_field().text()

        if len(new_collection_name) == 0:
            raise BadFieldValueException("Must enter valid collection name")

        else:
            return new_collection_name

    def create_new_collection(self):
        try:
            new_collection_name = self.get_new_collection_name()

            self.db.create_new_collection(new_collection_name)

            self.update_collection_list()

            msg = f"Created collection: {new_collection_name}"
            self.msg = PopupTextmessage(self, text=msg)

        except BadFieldValueException:
            self.msg = PopupTextmessage(self, "Must provide valid collection name first")


    def _is_last_collection(self):
        return len(self.collection_list) == 1

    def _drop_selected_collection(self, selected_collection, is_last=False):
            
        self.db.drop_selected_collection(selected_collection, is_last=is_last)

        if is_last:
            self.clear_collection_list()
            self.update_information_labels(with_default=True)
            self.close()

        else:
            self.update_collection_list()

    def drop_selected_collection(self):
        try:
            selected_collection = self.get_selected_collection()

            if self._is_last_collection():

                message = f"Warning! This will also drop this collection's database ({self.db.current_db.name})"
                callback = lambda: self._drop_selected_collection(selected_collection, is_last=True)

                self.msg = PopupConfirmBox(self, text=message, callback=callback)
            
            else:
                self._drop_selected_collection(selected_collection)

        except CollectionNotChosenYetException:
            self.msg = PopupTextmessage(self, "Must select a collection first")


    def export_collection(self):
        print("Button Clicked!")


    def show(self):
        if self.db.current_db is None:
            print("Must choose database before you can open the Collection Window")
            self.msg = PopupTextmessage(self, text="Must choose database before you can open the Collection Window")
            return
        else:
            return super().show()


# endregion Edit DB / Collection Buttons


# region CRUD Buttons

class CreateWindow(CRUDWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = CreateWindowListener(self, self.db)

        self.disable_id_field()

    def create_button_onclick(self):
        print("Clicked Create Button")


class FilterWindow(CRUDWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = FilterWindowListener(self, self.db)


class ModifyWindow(CRUDWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = ModifyWindowListener(self, self.db)

        self.disable_id_field()


class DeleteWindow(CRUDWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = DeleteWindowListener(self, self.db)

        self.disable_id_field()

# endregion CRUD Buttons


# region Function Buttons

class FunctionWindow(PopupWindow):
    def __init__(self, window_title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(window_title)

# endregion Function Buttons
