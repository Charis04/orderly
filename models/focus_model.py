# Focus model module
from peewee import *
from .task_model import Task, BaseModel
from datetime import datetime

class FocusSession(BaseModel):
    task = ForeignKeyField(Task, backref="focus_sessions")
    start_time = DateTimeField(default=datetime.now)
    end_time = DateTimeField(null=True)
    duration_minutes = IntegerField(null=True)

    def end_session(self):
        self.end_time = datetime.now()
        self.duration_minutes = int((self.end_time - self.start_time).total_seconds() // 60)
        self.save()
