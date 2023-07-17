from Frontend import *
import toolbox as util

class PopupWindow(Frontend):
    def __init__(self, parent_gui, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_gui = parent_gui
        self.msg = None
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
        super().__init__(parent_gui=parent, widget_ids=ids, gui_file_path=path_, db=None)
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


class CreateNewFieldWindow(PopupWindow):
    def __init__(self, field_names, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.event_listener = NewFieldWindowListener(self, self.db)

        self.name_lineEdit = self._get_name_lineEdit()
        self.type_comboBox = self._get_type_comboBox()

        self.field_names = field_names

    def _get_name_lineEdit(self):
        return self.widget_objects['fieldNameLineEdit']

    def _get_type_comboBox(self):
        return self.widget_objects['fieldTypeComboBox']

    @staticmethod
    def validate_field_name(field_name: str):
        if len(field_name) == 0:
            raise BadFieldValueException("No value detected for field name")

    def check_field_does_not_already_exist(self, field_name):
        if field_name in self.field_names:
            msg = "Cannot use name '" + field_name + "' Because it's already in use"
            raise FieldNameAlreadyInUseException(msg)

    def _get_field_name(self):

        field_name = self.name_lineEdit.text()

        self.validate_field_name(field_name=field_name)
        self.check_field_does_not_already_exist(field_name=field_name)

        return field_name

    def _get_field_type(self):

        field_type = self.type_comboBox.currentText()
        print("Current chosen field type is " + field_type)

        return field_type

    def create_button_onclick(self):
        try:
            field_name = self._get_field_name()
            field_type = self._get_field_type()

            self.parent_gui.create_new_field(field_name, field_type)
            self.close()

        except FieldNameAlreadyInUseException:
            self.msg = PopupTextmessage(self, "Field name is already in use")

        except BadFieldValueException:
            self.msg = PopupTextmessage(self, "Must enter field name")


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
        self.db_count_label = None
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
            selected_collection = self.collection_list.selectedItems()[
                0].text()
            return selected_collection

        except IndexError:
            print("Must select a collection first!")
            raise CollectionNotChosenYetException(
                "Must select a collection first")

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

            self.db.change_collection_name(
                selected_collection, new_collection_name)

            self.update_collection_list()
            self.update_information_labels(with_default=True)

        except CollectionNotChosenYetException:
            self.msg = PopupTextmessage(self, "Must select a collection first")

        except BadFieldValueException:
            self.msg = PopupTextmessage(
                self, "Must provide a new name for collection")

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
            self.msg = PopupTextmessage(
                self, "Must provide valid collection name first")

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
                def callback(): return self._drop_selected_collection(
                    selected_collection, is_last=True)

                self.msg = PopupConfirmBox(
                    self, text=message, callback=callback)

            else:
                self._drop_selected_collection(selected_collection)

        except CollectionNotChosenYetException:
            self.msg = PopupTextmessage(self, "Must select a collection first")

    @staticmethod
    def export_collection():
        print("Button Clicked!")

    def show(self):
        if self.db.current_db is None:
            print("Must choose database before you can open the Collection Window")
            self.msg = PopupTextmessage(
                self, text="Must choose database before you can open the Collection Window")
            return
        else:
            return super().show()

# region Function Buttons


class FunctionWindow(PopupWindow):
    def __init__(self, window_title, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(window_title)

# endregion Function Buttons
