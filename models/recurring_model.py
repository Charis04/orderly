# Recurring model module
from peewee import *
from .database import db
import datetime

class RecurringTask(Model):
    title = CharField()
    category = CharField()
    description = TextField(null=True)
    recurrence_type = CharField(choices=[
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
    ])  # "daily", "weekly", "monthly"
    start_date = DateField()
    end_date = DateField(null=True)
    last_generated = DateField(null=True)

    class Meta:
        database = db

    def __str__(self):
        return f"{self.title} - {self.category} - {self.recurrence_type} - Start: {self.start_date} - End: {self.end_date} - Last Generated: {self.last_generated}"

    def __repr__(self):
        return f"RecurringTask({self.title}, {self.category}, {self.recurrence_type}, {self.start_date}, {self.end_date}, {self.last_generated})"
