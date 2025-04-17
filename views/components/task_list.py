from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtCore import Signal, Qt

class TaskList(QListWidget):
    task_toggled = Signal(int, bool)  # task_id

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
                border-radius: 6px;
            }
        """)
        self.itemClicked.connect(self.toggle_task)

    def populate(self, tasks):
        self.clear()
        for task in tasks:
            item = QListWidgetItem(f"{task.title} ({task.category}) - Due {task.due_date}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if task.completed else Qt.Unchecked)
            item.setData(1, task.id)
            self.addItem(item)

    def toggle_task(self, item):
        task_id = item.data(1)
        completed = item.checkState() == Qt.Checked
        print("Task toggled:", task_id, "Completed:", completed)  # Debugging line
        self.task_toggled.emit(task_id, not completed)
