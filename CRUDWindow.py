from Frontend import *
from PopupWindow import PopupWindow, PopupTextmessage, CreateNewFieldWindow


class CRUDWindow(PopupWindow):
    def __init__(self, disable_field_edit=False, fields=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if fields is None:
            fields = []
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
        [label.setText(str(text)) for label, text in zip(
            self.labels.values(), self.label_values)]
        [field.setText(str(text)) for field, text in zip(
            self.fields.values(), self.field_values)]

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
        [self.fields_container_layout.addWidget(
            label, index, 0) for index, label in self._label_widgets()]
        [self.fields_container_layout.addWidget(
            field, index, 1) for index, field in self._field_widgets()]

    def clear_layout(self):
        while not self.fields_container_layout.isEmpty():
            # According to some guy on the internet, this stops memory leaks
            # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt/13103617
            self.fields_container_layout.itemAt(0).widget().deleteLater()
            self.fields_container_layout.itemAt(0).widget().setParent(None)

    def _make_widgets(self):
        label_widgets = [QLabel(col_name) for col_name in self.label_values]
        field_widgets = [QLineEdit() for _ in self.label_values]

        paired_label_values = {str(widget_text): widget for widget_text, widget in zip(
            self.label_values, label_widgets)}
        paired_field_values = {str(widget_text): widget for widget_text, widget in zip(
            self.label_values, field_widgets)}

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
        template = self.db.current_collection.get_field_types()

        label_values = list(template.keys())
        field_values = list(template.values())

        return label_values, field_values

    def set_fields(self):
        self._check_current_collection()

        try:
            self.label_values, self.field_values = self._get_label_and_field_values()
            self._set_fields()

        except EmptyCollectionException:
            self._set_fields(empty_collection=True)

    def disable_id_field(self):
        try:
            self.disable_field('_id')

        except KeyError as e:
            # Likely empty collection
            print(e)
            pass

        except RuntimeError as r:
            # This happens because '_id' key is present but referenced object is deleted
            print(r)
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

        except CollectionNotChosenYetException:
            self.msg = PopupTextmessage(
                self, text="Must choose Database and Collection First")
            print("Cannot open CRUD window without choosing a collection first")
            return


# endregion Base Classes

# region CRUD Buttons

class CreateWindow(CRUDWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = CreateWindowListener(self, self.db)

        self.new_fields_added = False
        self.new_field_types = {}
        self.new_field_button = self.get_new_field_button()

        self.disable_id_field()

    def set_fields(self):
        super().set_fields()
        self.disable_id_field()

    def get_new_field_button(self):
        return self.widget_objects['newFieldButton']

    def get_formatted_query_data(self):
        """
        Returns dict of field labels and field values (minus _id field)
        """

        data = self.fields
        formatted_data = {key: value.text() for key, value in data.items()}

        formatted_data.pop('_id')

        return formatted_data

    def get_current_field_names(self):
        return self.label_values

    def new_field_button_onclick(self):
        widgets = util.json_to_dict("widget_ids/NEW_FIELD_WIDGET_ID.json")
        path_to_gui = "ui/new_field_gui.ui"
        field_names = self.get_current_field_names()

        self.new_field_window = CreateNewFieldWindow(field_names=field_names,
                                                     parent_gui=self,
                                                     gui_file_path=path_to_gui,
                                                     widget_ids=widgets,
                                                     db=self.db
                                                     )

        self.new_field_window.show()

    def add_id_field(self):
        new_field_label = QLabel('_id')
        new_field_lineEdit = QLineEdit(self)

        # Update value lists
        self.label_values.append('_id')
        self.field_values.append("")

        # Update widget dictionary
        self.fields['_id'] = new_field_lineEdit

        self.fields_container_layout.addWidget(new_field_label, 0, 0)
        self.fields_container_layout.addWidget(new_field_lineEdit, 0, 1)

        new_field_lineEdit.setDisabled(True)

    def check_empty_layout(self):
        """
        If True, then _id field must be added because it didn't exist
        before the last field was added
        """
        return len(self.fields) == 1

    def add_new_field(self, field_name):

        # BUG Potential. This needs a lot of testing

        new_field_label = QLabel(field_name)
        new_field_lineEdit = QLineEdit(self)

        # Update value lists
        self.label_values.append(field_name)
        self.field_values.append("")

        # Update widget dictionary
        self.fields[field_name] = new_field_lineEdit

        if self.check_empty_layout():
            self.clear_layout()
            self.add_id_field()

        row_index = len(self.label_values)
        self.fields_container_layout.addWidget(new_field_label, row_index, 0)
        self.fields_container_layout.addWidget(
            new_field_lineEdit, row_index, 1)

        self.new_fields_added = True

    def set_new_field_type(self, field_name, field_type):

        if field_type == "string":
            self.new_field_types[field_name] = "str"

        elif field_type == "int":
            self.new_field_types[field_name] = "int"

        elif field_type == "float":
            self.new_field_types[field_name] = "float"

        else:
            raise BadFieldTypeException(
                "type must be 'str', 'int', or 'float'")

    def create_new_field(self, field_name, field_type):
        print("\nNew Field Info")
        print(f"Field Name: {field_name}")
        print(f"Field Type: {field_type}\n")

        self.set_new_field_type(field_name, field_type)
        self.add_new_field(field_name)

    def create_button_onclick(self):
        formatted_data = self.get_formatted_query_data()

        if self.new_fields_added:

            custom_types = self.new_field_types()

            created_id = self.db.create_query(
                data=formatted_data,
                callback=print_id,
                custom_types_flag=True,
                custom_types=custom_types)

        else:

            created_id = self.db.create_query(
                data=formatted_data, callback=print_id)



class FilterWindow(CRUDWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = FilterWindowListener(self, self.db)


class ModifyWindow(CRUDWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = ModifyWindowListener(self, self.db)

    def set_fields(self):
        super().set_fields()
        self.disable_id_field()


class DeleteWindow(CRUDWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._event_listener = DeleteWindowListener(self, self.db)

    def set_fields(self):
        super().set_fields()
        self.disable_id_field()

# endregion CRUD Buttons
