# Database module
from peewee import SqliteDatabase

# SQLite database file
db = SqliteDatabase('task_manager.db')

def init_db():
    from models.task_model import Task  # Avoid circular import
    db.connect()
    db.create_tables([Task], safe=True)
