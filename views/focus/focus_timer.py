# Focus timer module
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QHBoxLayout
)
from PySide6.QtCore import QTimer, QTime, Qt
from models.task_model import Task
from models.focus_model import FocusSession

class FocusTimer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Focus Timer")
        self.setMinimumSize(300, 300)
        #self.setStyleSheet("background-color: #f0f0f0;")
        self.setContentsMargins(10, 10, 10, 10)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.session = None
        self.timer = QTimer()
        self.elapsed = QTime(0, 0, 0)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.task_selector = QComboBox()
        self.load_tasks()

        self.time_display = QLabel("00:00:00")
        self.time_display.setStyleSheet("font-size: 32px;")

        self.start_btn = QPushButton("Start Focus")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)

        layout.addWidget(QLabel("Select a task to focus on:"))
        layout.addWidget(self.task_selector)
        layout.addWidget(self.time_display)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)

        self.timer.timeout.connect(self.update_timer)
        self.start_btn.clicked.connect(self.start_focus)
        self.stop_btn.clicked.connect(self.stop_focus)

    def load_tasks(self):
        self.task_selector.clear()
        for task in Task.select().where(Task.completed == False):
            self.task_selector.addItem(task.title, task.id)

    def update_timer(self):
        self.elapsed = self.elapsed.addSecs(1)
        self.time_display.setText(self.elapsed.toString("hh:mm:ss"))

    def start_focus(self):
        task_id = self.task_selector.currentData()
        task = Task.get_by_id(task_id)
        self.session = FocusSession.create(task=task)
        self.elapsed = QTime(0, 0, 0)
        self.timer.start(1000)
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_focus(self):
        self.timer.stop()
        if self.session:
            self.session.end_session()
        self.time_display.setText("00:00:00")
        self.session = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
