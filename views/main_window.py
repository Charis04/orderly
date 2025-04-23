from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from controllers.task_controller import TaskController
from views.components.form import TaskForm
from views.components.task_list import TaskList
from views.components.side_bar import Sidebar
from views.task_details import TaskDetailView
from utils.recurrence import generate_recurring_tasks

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Orderly - Task Manager")
        self.setMinimumSize(900, 600)

        self.controller = TaskController()

        self.task_form = TaskForm()
        self.task_form.hide()
        self.task_list = TaskList()
        self.side_bar = Sidebar()
        self.task_detail_view = TaskDetailView(self)
        self.task_detail_view.hide()

        self.task_form.task_added.connect(self.handle_task_added)
        self.task_list.task_toggled.connect(self.handle_task_toggled)
        self.side_bar.view_changed.connect(self.handle_view_change)
        self.side_bar.add_task_clicked.connect(self.show_task_form)

        self.current_view = "today"  # Default view
        self.init_ui()
        self.load_tasks()

    def init_ui(self):
        main_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.side_bar, 1)

        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(15)

        content_layout.addWidget(QLabel("Your Tasks:"))
        content_layout.addWidget(self.task_list)

        content.setLayout(content_layout)
        layout.addWidget(content, 4)
        layout.addWidget(self.task_form, 1)
        layout.addWidget(self.task_detail_view, 2)


        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Set styles for the components
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 6px;
            }

            QWidget {
                background-color: #f8f9fa;
                font-family: "Segoe UI", sans-serif;
            }
        """)

    def load_tasks(self):
        generate_recurring_tasks()
        tasks = self.controller.get_tasks_by_view(self.current_view)
        self.task_list.populate(tasks)

    def handle_task_added(self, task_data):
        self.controller.create_task(task_data)
        self.task_form.hide()
        self.load_tasks()

    def handle_task_toggled(self, task_id):
        task = self.controller.get_task_by_id(task_id)
        if task:
            self.task_detail_view.load_task(task)
            self.load_tasks()

    def handle_view_change(self, view_name):
        self.current_view = view_name
        self.load_tasks()

    def show_task_form(self):
        self.task_form.show()
