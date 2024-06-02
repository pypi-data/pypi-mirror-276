# -*- coding: utf-8 -*-

from typing import Optional, Dict, AnyStr, Union

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (QDialog, QWidget, QTableWidget, QPushButton, QSpacerItem, QHBoxLayout, QVBoxLayout,
                               QSizePolicy, QTableWidgetItem, QHeaderView, QLabel)

from ezcoding.generator import Generator
from ezcoding.utils import is_built_in_variable
from ezcoding.const import TEMPLATE_KEY


def set_table_item_not_editable(item: QTableWidgetItem):
    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)


class EditorUI(object):

    KEY_INDEX: int = 0
    VALUE_INDEX: int = 1
    RESET_INDEX: int = 2

    COLUMN_COUNT: int = 3

    def __init__(self, editor: QDialog):
        editor.setMinimumSize(960, 360)
        editor.setWindowTitle('Variable Value Editor')
        editor.setSizeGripEnabled(True)

        self.template = QLabel('Template: ', editor)
        self.template.setFixedHeight(18)
        self.template.setFont(QFont('Consolas', 10))
        self.template.setOpenExternalLinks(True)

        self.table = QTableWidget(editor)
        self.table.setColumnCount(self.COLUMN_COUNT)
        self.table.setHorizontalHeaderLabels(['Variable', 'Value', 'Reset'])
        self.table.setColumnWidth(self.KEY_INDEX, 128)
        self.table.horizontalHeader().setSectionResizeMode(self.VALUE_INDEX, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(self.RESET_INDEX, 64)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.apply = QPushButton('Apply', editor)
        self.apply.setToolTip('Generate file using changed values')
        self.apply.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.discard = QPushButton('Discard', editor)
        self.discard.setToolTip('Discard value changes and generate file')
        self.discard.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.bottom_spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setSpacing(8)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(8, 8, 8, 8)

        self.bottom_layout.addSpacerItem(self.bottom_spacer)
        self.bottom_layout.addWidget(self.apply)
        self.bottom_layout.addWidget(self.discard)

        self.layout.addWidget(self.template)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.bottom_layout)

        editor.setLayout(self.layout)


class Editor(QDialog):

    def __init__(self, values: Dict[AnyStr, Union[AnyStr, Generator]], parent: Optional[QWidget] = None,
                 flags: Qt.WindowType = Qt.WindowType.Dialog):
        super().__init__(parent, flags)
        self.__ui = EditorUI(self)
        self.__load_table(values)
        self.__values: Dict[AnyStr, Union[AnyStr, Generator]] = values
        self.__bind_signals()

    def __load_table(self, values: Dict[AnyStr, Union[AnyStr, Generator]]):
        if TEMPLATE_KEY in values:
            template_path = values[TEMPLATE_KEY]
            self.__ui.template.setText(f'{self.__ui.template.text()} <a href="{template_path}">{template_path}</a>')

        self.__ui.table.setRowCount(len(values))
        font = QFont('Consolas', 10)
        row_index = 0
        for variable in values:
            value_text = values[variable]
            not_editable = is_built_in_variable(variable)

            variable_item = QTableWidgetItem(variable)
            variable_item.setFont(font)
            set_table_item_not_editable(variable_item)
            self.__ui.table.setItem(row_index, EditorUI.KEY_INDEX, variable_item)

            value_item = QTableWidgetItem(value_text)
            value_item.setFont(font)
            if not_editable:
                set_table_item_not_editable(value_item)
            self.__ui.table.setItem(row_index, EditorUI.VALUE_INDEX, value_item)

            if not_editable:
                reset_item = QTableWidgetItem()
                set_table_item_not_editable(reset_item)
                self.__ui.table.setItem(row_index, EditorUI.RESET_INDEX, reset_item)
            else:
                reset_button = QPushButton('Reset')
                reset_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                self.__ui.table.setCellWidget(row_index, EditorUI.RESET_INDEX, reset_button)

            row_index += 1

    def __bind_signals(self):
        self.__ui.apply.clicked.connect(self.__on_apply_clicked)
        self.__ui.discard.clicked.connect(self.__on_discard_clicked)

        rows = self.__ui.table.rowCount()
        for row in range(rows):
            button = self.__ui.table.cellWidget(row, EditorUI.RESET_INDEX)
            if isinstance(button, QPushButton):
                button.clicked.connect(self.__on_reset_clicked)

    def __update_values(self):
        rows = self.__ui.table.rowCount()
        for i in range(rows):
            variable = self.__ui.table.item(i, EditorUI.KEY_INDEX).text()
            value = self.__values[variable]
            if not isinstance(value, str):
                continue
            value = self.__ui.table.item(i, EditorUI.VALUE_INDEX).text()
            self.__values[variable] = value

    @Slot(bool)
    def __on_reset_clicked(self, checked: bool):
        target_button = self.sender()
        rows = self.__ui.table.rowCount()
        for row in range(rows):
            button = self.__ui.table.cellWidget(row, EditorUI.RESET_INDEX)
            if button == target_button:
                key = self.__ui.table.item(row, EditorUI.KEY_INDEX).text()
                value = self.__values[key]
                if isinstance(value, str):
                    self.__ui.table.item(row, EditorUI.VALUE_INDEX).setText(value)
                break

    @Slot(bool)
    def __on_apply_clicked(self, checked: bool):
        self.__update_values()
        self.close()

    @Slot(bool)
    def __on_discard_clicked(self, checked: bool):
        self.close()
