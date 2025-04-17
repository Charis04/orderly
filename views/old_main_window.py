from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget,
    QComboBox, QDateEdit, QMessageBox
)
from PySide6.QtCore import QDate
from controllers.task_controller import TaskController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orderly")
        self.setMinimumSize(900, 600)

        self.controller = TaskController()

        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        # Add padding around the layout
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Form Section ---
        form_layout = QHBoxLayout()
        form_layout.setSpacing(15)

        # Title input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title")
        self.title_input.setStyleSheet("padding: 5px; font-size: 14px;")
        form_layout.addWidget(self.title_input)

        # Category combo box
        self.category_combo = QComboBox()
        self.category_combo.addItems(["general", "daily", "weekly", "monthly"])
        self.category_combo.setStyleSheet("padding: 5px; font-size: 14px;")
        self.category_combo.setPlaceholderText("Select category")
        form_layout.addWidget(self.category_combo)

        # Due date picker
        self.due_date_picker = QDateEdit()
        self.due_date_picker.setDate(QDate.currentDate())
        self.due_date_picker.setCalendarPopup(True)
        self.due_date_picker.setStyleSheet("padding: 5px; font-size: 14px;")
        form_layout.addWidget(self.due_date_picker)

        # Add task button
        self.add_btn = QPushButton("Add Task")
        self.add_btn.clicked.connect(self.handle_add_task)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        form_layout.addWidget(self.add_btn)

        # --- Task List Section ---
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                background-color: #f4f4f4;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 10px;
                margin-bottom: 5px;
            }
            QListWidget::item:selected {
                background-color: #B0E0E6;
            }
        """)
        self.task_list.itemClicked.connect(self.toggle_task_status)  # Connect to click handler

        # Add to main layout
        main_layout.addLayout(form_layout)
        main_layout.addWidget(QLabel("Your Tasks:"))
        main_layout.addWidget(self.task_list)

        # Apply the layout to the main widget
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Apply overall window styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 16px;
                color: #333;
                margin-bottom: 10px;
            }
        """)

    def handle_add_task(self):
        title = self.title_input.text().strip()
        category = self.category_combo.currentText()
        due_date = self.due_date_picker.date().toPython()

        if not title:
            QMessageBox.warning(self, "Missing Title", "Please enter a task title.")
            return

        self.controller.create_task(
            title=title,
            category=category,
            due_date=due_date
        )

        self.title_input.clear()
        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()
        tasks = self.controller.get_all_tasks()
        for task in tasks:
            status = "[✔]" if task.completed else "[ ]"
            self.task_list.addItem(f"{status} {task.title} ({task.category}) - Due {task.due_date}")
            self.task_list.item(self.task_list.count() - 1).setData(1, task.id)  # Store task ID in item data

    def toggle_task_status(self, item):
        task_id = item.data(1)  # Retrieve task id from the item
        task = self.controller.get_task_by_id(task_id)

        if task:
            # Toggle completion status
            new_status = not task.completed
            updated_task = self.controller.update_task_status(task_id, completed=new_status)

            if updated_task:
                self.load_tasks()
