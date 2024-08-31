from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,QMainWindow,QMessageBox,QVBoxLayout,QPushButton,QListWidget,QLineEdit,
    QDateEdit,QHBoxLayout,QLabel)
from PySide6.QtCore import QDate
import datetime
import os
import platform
from plyer import notification


class TodoApp (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To do Scheduler")


        self.todo_list = QListWidget(self)

        delete_button = QPushButton("Delete Task")

        #self.delete_button.clicked.connect(self.delete_task)
        #delete_button.setShortcut("del")

        add_button = QPushButton("Add Task")
        #self.add_button.clicked.connect(self.show_add)

        #b_laout = QHBoxLayout()
        #b_laout.addWidget(add_button)
        #b_laout.addWidget(delete_button)

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.todo_list)
        list_layout.addWidget(add_button)
        list_layout.addWidget(delete_button)
        self.setLayout(list_layout)


    