# Focus timer module
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox
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
        self.session = None
        self.timer = QTimer()
        self.duration = 60  # Default duration in minutes
        self.remaining_seconds = self.duration * 60
        self.elapsed = QTime(0, 0, 0)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Label for task selection
        layout.addWidget(QLabel("Select a task to focus on:"))
        self.task_selector = QComboBox()
        self.load_tasks()
        layout.addWidget(self.task_selector)

        # SpinBox for selecting session length
        self.duration_selector = QSpinBox()
        self.duration_selector.setRange(5, 720)
        self.duration_selector.setSingleStep(5)
        self.duration_selector.setValue(self.duration)
        self.duration_selector.setSuffix(" min")
        self.duration_selector.valueChanged.connect(self.update_duration)
        layout.addWidget(QLabel("Set session length (minutes):"))
        layout.addWidget(self.duration_selector)

        # Display for session length
        self.time_display = QLabel(f"{self.duration}:00")
        self.time_display.setStyleSheet("font-size: 32px;")
        self.time_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_display)

        # Buttons to control the timer
        self.start_btn = QPushButton("Start Focus")
        layout.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.start_focus)
        self.pause_btn = QPushButton("Pause")
        layout.addWidget(self.pause_btn)
        self.pause_btn.setVisible(False)
        self.pause_btn.clicked.connect(self.pause_focus)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)
        self.stop_btn.clicked.connect(self.stop_focus)
        

        self.setLayout(layout)

        self.timer.timeout.connect(self.update_timer)

    def load_tasks(self):
        self.task_selector.clear()
        for task in Task.select().where(Task.completed == False):
            self.task_selector.addItem(task.title, task.id)

    def update_duration(self, value):
        self.duration = value
        self.remaining_seconds = self.duration * 60
        self.update_timer_display()

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_display()
        else:
            self.timer.stop()
            self.time_display.setText("Session Complete!")

    def update_timer_display(self):
        mins, secs = divmod(self.remaining_seconds, 60)
        self.time_display.setText(f"{mins:02d}:{secs:02d}")

    def start_focus(self):
        task_id = self.task_selector.currentData()
        task = Task.get_by_id(task_id)
        self.session = FocusSession.create(task=task)
        self.remaining_seconds = self.duration * 60
        self.update_timer_display()
        self.timer.start(1000)
        self.start_btn.setEnabled(False)
        self.pause_btn.setVisible(True)
        self.stop_btn.setEnabled(True)
        self.duration_selector.setEnabled(False)
        self.task_selector.setEnabled(False)
    
    def pause_focus(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_btn.setText("Resume")
        else:
            self.timer.start(1000)
            self.pause_btn.setText("Pause")
        self.stop_btn.setEnabled(True)

    def stop_focus(self):
        self.timer.stop()
        if self.session:
            self.session.end_session()
        self.time_display.setText("00:00:00")
        self.session = None
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.pause_btn.setText("Pause")
        self.pause_btn.setVisible(False)
        self.duration_selector.setEnabled(True)
        self.task_selector.setEnabled(True)
