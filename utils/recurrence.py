# Recurrence module
from datetime import date, timedelta
from models.recurring_model import RecurringTask
from models.task_model import Task

def generate_recurring_tasks():
    today = date.today()
    rec_tasks = RecurringTask.select()

    for rec in rec_tasks:
        next_date = rec.last_generated or rec.start_date
        while next_date <= today:
            if rec.end_date and next_date > rec.end_date:
                break

            # Prevent duplicates
            exists = Task.select().where(
                (Task.title == rec.title) &
                (Task.category == rec.category) &
                (Task.due_date == next_date)
            ).exists()

            if not exists:
                Task.create(
                    title=rec.title,
                    category=rec.category,
                    due_date=next_date,
                    description=rec.description,
                    is_recurring=True,
                    completed=False
                )

            # Move next_date forward based on recurrence_type
            if rec.recurrence_type == 'daily':
                next_date += timedelta(days=1)
            elif rec.recurrence_type == 'weekly':
                next_date += timedelta(weeks=1)
            elif rec.recurrence_type == 'monthly':
                next_date = _add_month(next_date)
            else:
                break  # skip invalid type

        # Update last_generated
        if rec.last_generated != today:
            rec.last_generated = today
            rec.save()

def _add_month(d):
    """Handles month rolling (naive version)."""
    month = d.month + 1 if d.month < 12 else 1
    year = d.year + (1 if month == 1 else 0)
    day = min(d.day, 28)  # Avoid invalid days (Feb 30, etc.)
    return date(year, month, day)
