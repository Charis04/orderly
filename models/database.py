# Database module
from peewee import SqliteDatabase

# SQLite database file
db = SqliteDatabase('orderly.db')

def init_db():
    from models.task_model import Task
    from models.recurring_model import RecurringTask
    from models.focus_model import FocusSession
    # Avoid circular import
    db.connect()
    db.create_tables([Task, RecurringTask, FocusSession], safe=True)
