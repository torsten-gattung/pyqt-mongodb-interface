from Frontend import *
from PopupWindow import PopupWindow, PopupTextmessage


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
        except IndexError:
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
        # BUG #6: Program will crash if a new database is created with a name already in use

        db_name_input = self.widget_objects['databaseNameInput']
        # selected_template = self.widget_objects['templateList'].selectedItems()[0]

        database_name = db_name_input.text()
        # database_template = selected_template.text()

        self.db.create_new_database(db_name=database_name, template=None)

        self.update_database_list()
        self.msg = PopupTextmessage(self, f"Created Database: {database_name}")

    def delete_selected_database(self):

        # BUG #7: Database will not be deleted unless highlighted in list before
        # BUG #7: This happens because the db list is being emptied and filled everytime the window is opened

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


# endregion Edit DB / Collection Buttons
