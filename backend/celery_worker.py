from celery import Celery


celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


celery.conf.task_routes = {
    "tasks.*": {"queue": "default"}
}

from celery.schedules import crontab

celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'tasks.daily_reminders',
        'schedule': crontab(hour=8, minute=0), # Daily at 8:00 AM
    },
    'send-monthly-report': {
        'task': 'tasks.monthly_report_task',
        'schedule': crontab(day_of_month=1, hour=0, minute=0), # 1st of every month
    },
}