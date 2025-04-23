# Task model module
from peewee import *
from .database import db

class BaseModel(Model):
    class Meta:
        database = db

class Task(BaseModel):
    id = AutoField()
    title = CharField()
    description = TextField(null=True)
    due_date = DateField(null=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    completed = BooleanField(default=False)
    category = CharField(choices=[
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
    ])
    is_recurring = BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.category} - Due: {self.due_date} - {'Completed' if self.completed else 'Pending'}"
    
    def __repr__(self):
        return f"Task({self.id}, {self.title}, {self.category}, {self.due_date}, {'Completed' if self.completed else 'Pending'})"
