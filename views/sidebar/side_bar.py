# views/components/sidebar.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Signal

class Sidebar(QWidget):
    view_changed = Signal(str)  # Emits "today", "week", "month", or "all"
    add_task_clicked = Signal()  # Emits when "Add Task" is clicked
    focus_timer_clicked = Signal()  # Emits when "Focus Session" is clicked

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        self.setStyleSheet("""
            QPushButton {
                padding: 10px;
                text-align: left;
                font-size: 14px;
                background-color: #f0f0f0;
                border: none;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: #d0eaff;
            }

            QPushButton:checked {
                background-color: #007ACC;
                color: white;
                font-weight: bold;
            }
        """)

        self.buttons = {}
        for name, label in {
            "today": "Today's Tasks",
            "week": "This Week",
            "month": "This Month",
            "recurring": "Recurring Tasks",
            "all": "All Tasks"
        }.items():
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, n=name: self.change_view(n))
            layout.addWidget(btn)
            self.buttons[name] = btn

        self.add_task_btn = QPushButton("Add Task")
        self.add_task_btn.setCheckable(False)
        self.add_task_btn.setObjectName("addTaskButton")
        self.add_task_btn.clicked.connect(self.add_task_clicked.emit)
        layout.addWidget(self.add_task_btn)

        self.focus_btn = QPushButton("Focus Session")
        self.focus_btn.clicked.connect(self.focus_timer_clicked.emit)
        layout.addWidget(self.focus_btn)

        self.setLayout(layout)
        self.change_view("today")  # default selection

        # 🧩 Add spacer to push buttons to top
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def change_view(self, name):
        for key, btn in self.buttons.items():
            btn.setChecked(key == name)
        self.view_changed.emit(name)
