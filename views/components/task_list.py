from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Signal

class TaskList(QListWidget):
    task_toggled = Signal(int)  # task_id

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
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
        self.itemClicked.connect(self.toggle_task)

    def populate(self, tasks):
        self.clear()
        for task in tasks:
            status = "[✔]" if task.completed else "[ ]"
            item = QListWidgetItem(f"{status} {task.title} ({task.category}) - Due {task.due_date}")
            item.setData(0, task.id)
            self.addItem(item)

    def toggle_task(self, item):
        task_id = item.data(0)
        self.task_toggled.emit(task_id)
