# Time utils module
from datetime import date, timedelta

def categorize_task(due_date):
    today = date.today()
    if due_date == today:
        return "Today"
    elif today <= due_date <= today + timedelta(days=6 - today.weekday()):
        return "This Week"
    elif due_date.month == today.month and due_date.year == today.year:
        return "This Month"
