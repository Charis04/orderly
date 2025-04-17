# Task controller module
from models.task_model import Task
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
        all_tasks = self.get_all_tasks()
        today = date.today()

        if view == "today":
            return [t for t in all_tasks if t.due_date == today or t.category == "daily"]
        elif view == "week":
            end = today + timedelta(days=7)
            return [t for t in all_tasks if today <= t.due_date <= end or t.category == "weekly"]
        elif view == "month":
            end = today.replace(day=28) + timedelta(days=4)  # crude way to get next month
            end = end.replace(day=1) - timedelta(days=1)
            return [t for t in all_tasks if t.due_date.month == today.month or t.category == "monthly"]
        return all_tasks

    def get_tasks_by_category(self, category):
        return list(Task.select().where(Task.category == category))

    def get_tasks_due_today(self):
        today = date.today()
        return list(Task.select().where(Task.due_date == today))

    def create_task(self, title, description="", due_date=None, category="general", is_recurring=False):

        if category != "general":
            is_recurring = True
        task = Task.create(
            title=title,
            description=description,
            due_date=due_date,
            category=category,
            is_recurring=is_recurring
        )
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
