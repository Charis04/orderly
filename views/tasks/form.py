from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton,
    QHBoxLayout, QCheckBox, QComboBox, QDateEdit, QTextEdit
)
from PySide6.QtCore import QDate, Signal
from datetime import date
from utils.time_utils import categorize_task

class TaskForm(QWidget):
    task_added = Signal(dict)  # Emit a dictionary with task data
    task_updated = Signal(dict)  # Emit a dictionary with updated task data
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Top bar with close button
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        self.close_button = QPushButton("✖")
        self.close_button.setFixedSize(24, 24)
        self.close_button.setStyleSheet("border: none; font-weight: bold;")
        self.close_button.clicked.connect(self.hide)
        top_bar.addWidget(QLabel("Add Task"))
        top_bar.addWidget(self.close_button)
        layout.addLayout(top_bar)

        self.title_input = QLineEdit()
        self.description = QTextEdit()
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate())

        # Recurrence controls
        self.recurring_checkbox = QCheckBox("This is a recurring task")
        self.recurrence_type = QComboBox()
        self.recurrence_type.addItems(["Daily", "Weekly", "Monthly"])
        self.recurrence_type.setEnabled(False)

        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setEnabled(False)

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setEnabled(False)

        # Connect enabling/disabling
        self.recurring_checkbox.stateChanged.connect(self.toggle_recurrence_options)

        layout.addWidget(QLabel("Title"))
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Description"))
        layout.addWidget(self.description)

        layout.addWidget(QLabel("Due Date"))
        layout.addWidget(self.due_date_input)

        layout.addWidget(self.recurring_checkbox)
        layout.addWidget(QLabel("Recurrence Type"))
        layout.addWidget(self.recurrence_type)
        layout.addWidget(QLabel("Start Date"))
        layout.addWidget(self.start_date_input)
        layout.addWidget(QLabel("End Date (optional)"))
        layout.addWidget(self.end_date_input)

        self.save_button = QPushButton("Save Task")
        self.save_button.clicked.connect(self.get_form_data)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def toggle_recurrence_options(self, state):
        enabled = state == 2  # Checked
        self.recurrence_type.setEnabled(enabled)
        self.start_date_input.setEnabled(enabled)
        self.end_date_input.setEnabled(enabled)

    def get_form_data(self):
        data = {
            "title": self.title_input.text(),
            "description": self.description.toPlainText(),
            "category": categorize_task(self.due_date_input.date().toPython()),
            "due_date": self.due_date_input.date().toPython(),
            "recurring": self.recurring_checkbox.isChecked()
        }

        if data["recurring"]:
            data["recurrence_type"] = self.recurrence_type.currentText().lower()
            data["start_date"] = self.start_date_input.date().toPython()
            data["end_date"] = self.end_date_input.date().toPython() if self.end_date_input.date().isValid() else None

        self.task_added.emit(data)
