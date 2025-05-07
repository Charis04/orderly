from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QDateEdit, QHBoxLayout, QLineEdit, QSpacerItem, QSizePolicy, QTextEdit
)
from PySide6.QtCore import QDate, Signal
from models.task_model import Task
from models.recurring_model import RecurringTask

class TaskDetailView(QWidget):
    task_updated = Signal()  # Emit when the task is updated
    task_deleted = Signal()  # Emit when the task is deleted
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task = None
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Top bar with close button
        top_bar = QHBoxLayout()
        self.close_button = QPushButton("✖")
        self.close_button.setFixedSize(24, 24)
        self.close_button.setStyleSheet("border: none; font-weight: bold;")
        self.close_button.clicked.connect(self.hide)
        top_bar.addWidget(QLabel("Task Details"))
        top_bar.addStretch()
        top_bar.addWidget(self.close_button)
        self.layout.addLayout(top_bar)

        # Task details section
        details = QVBoxLayout()
        self.title_label = QLabel("Title")
        self.title = QLineEdit()
        self.description = QTextEdit()
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.completed_checkbox = QCheckBox("Completed")
        details.addWidget(self.title_label)
        details.addWidget(self.title)
        details.addWidget(QLabel("Description"))
        details.addWidget(self.description)
        details.addWidget(QLabel("Due Date:"))
        details.addWidget(self.due_date_input)
        details.addWidget(self.completed_checkbox)
        self.layout.addLayout(details)

        # Buttons for saving and deleting the task
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Changes")
        self.delete_button = QPushButton("Delete Task")
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.delete_button)
        self.layout.addLayout(buttons_layout)

        self.setLayout(self.layout)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.save_button.clicked.connect(self.update_task)
        self.delete_button.clicked.connect(self.delete_task)

    def load_task(self, task: Task):
        self.task = task
        if self.task.is_recurring:
            self.task = RecurringTask.select().where(
                RecurringTask.title == self.task.title).get()
            print("Task is recurring")
        self.title.setText(task.title)
        self.description.setPlainText(task.description)
        self.due_date_input.setDate(QDate(task.due_date.year, task.due_date.month, task.due_date.day))
        self.completed_checkbox.setChecked(task.completed)
        self.show()
        print(self.task.__class__)

    def update_task(self):
        if self.task:
            self.task.title = self.title.text()
            self.task.description = self.description.toPlainText()
            self.task.due_date = self.due_date_input.date().toPython()
            self.task.completed = self.completed_checkbox.isChecked()
            self.task.save()
            self.task_updated.emit()  # Emit signal to notify the parent

    def delete_task(self):
        if self.task:
            self.task.delete_instance()
            self.hide()
            self.task_deleted.emit()  # Emit signal to notify the parent
        self.task = None
