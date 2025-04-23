from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QDateEdit, QHBoxLayout
)
from PySide6.QtCore import QDate
from models.task_model import Task

class TaskDetailView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Top bar with close button
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        self.close_button = QPushButton("✖")
        self.close_button.setFixedSize(24, 24)
        self.close_button.setStyleSheet("border: none; font-weight: bold;")
        self.close_button.clicked.connect(self.hide)
        top_bar.addWidget(QLabel("Task Details"))
        top_bar.addWidget(self.close_button)
        self.layout.addLayout(top_bar)

        self.title_label = QLabel()
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)

        self.completed_checkbox = QCheckBox("Completed")
        self.save_button = QPushButton("Save Changes")
        self.delete_button = QPushButton("Delete Task")

        self.layout.addWidget(QLabel("Title:"))
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(QLabel("Due Date:"))
        self.layout.addWidget(self.due_date_input)
        self.layout.addWidget(self.completed_checkbox)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.delete_button)

        self.layout.addLayout(buttons_layout)
        self.setLayout(self.layout)

        self.save_button.clicked.connect(self.update_task)
        self.delete_button.clicked.connect(self.delete_task)

    def load_task(self, task: Task):
        self.task = task
        self.title_label.setText(task.title)
        self.due_date_input.setDate(QDate(task.due_date.year, task.due_date.month, task.due_date.day))
        self.completed_checkbox.setChecked(task.completed)
        self.show()

    def update_task(self):
        if self.task:
            self.task.due_date = self.due_date_input.date().toPython()
            self.task.completed = self.completed_checkbox.isChecked()
            self.task.save()

    def delete_task(self):
        if self.task:
            self.task.delete_instance()
            self.hide()
            self.parent().refresh_task_list()
