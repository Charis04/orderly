# Task controller module
from models.task_model import Task
from models.recurring_model import RecurringTask
from datetime import date, timedelta
from peewee import DoesNotExist

class TaskController:
    def __init__(self):
        pass  # Can inject logger, settings, etc.

    def get_all_tasks(self):
        return list(Task.select().order_by(Task.due_date))
    
    def get_task_by_id(self, task_id):
        try:
            return Task.get_by_id(task_id)
        except DoesNotExist:
            return None
        
    def get_tasks_by_view(self, view):

        if view == "today":
            return self.get_tasks_due_today()
        elif view == "week":
            self.get_tasks_by_category("week")
        elif view == "month":
            self.get_tasks_by_category("month")

        return self.get_all_tasks()

    def get_tasks_by_category(self, category):
        return list(Task.select().where(Task.category == category))

    def get_tasks_due_today(self):
        today = date.today()
        return list(Task.select().where(Task.due_date == today))

    def create_task(self, task_data):

        if task_data['recurring']:
            task = RecurringTask.create(**task_data)
        else:
            task = Task.create(**task_data)
            
        return task

    def update_task_status(self, task_id, completed=True):
        try:
            task = Task.get_by_id(task_id)
            task.completed = completed
            task.save()
            return task
        except DoesNotExist:
            return None

    def delete_task(self, task_id):
        try:
            task = Task.get_by_id(task_id)
            task.delete_instance()
            return True
        except DoesNotExist:
            return False
