from celery import Celery


celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


celery.conf.task_routes = {
    "tasks.*": {"queue": "default"}
}