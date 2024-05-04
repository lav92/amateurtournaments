from celery import Celery

from app.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER,
    include=["app.tasks.tasks", "app.stats.services"]
)
