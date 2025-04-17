from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QComboBox,
    QDateEdit, QPushButton
)
from PySide6.QtCore import QDate, Signal

class TaskForm(QWidget):
    task_added = Signal(str, str, QDate)  # title, category, due_date

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title")
        layout.addWidget(self.title_input)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["General", "Daily", "Weekly", "Monthly"])
        layout.addWidget(self.category_combo)

        self.due_date_picker = QDateEdit()
        self.due_date_picker.setDate(QDate.currentDate())
        self.due_date_picker.setCalendarPopup(True)
        layout.addWidget(self.due_date_picker)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.emit_task_data)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        # Set styles for the components
        self.setStyleSheet("""
            QLineEdit, QComboBox, QDateEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #007ACC;
                color: white;
                padding: 6px 12px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #005F99;
            }

            QPushButton:pressed {
                background-color: #004C7A;
            }
        """)

    def emit_task_data(self):
        title = self.title_input.text().strip()
        if title:
            self.task_added.emit(
                title,
                self.category_combo.currentText(),
                self.due_date_picker.date()
            )
            self.title_input.clear()
