from celery import Celery
from celery.schedules import crontab
import os
from flask import current_app
from dotenv import load_dotenv, find_dotenv

from app import create_app

ENV_FILE = find_dotenv(r".env")
load_dotenv(ENV_FILE)


def make_celery(app):
    """Create and configure Celery instance"""

    # Celery configuration
    celery_config = {
        "broker_url": os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1"),
        "result_backend": os.environ.get(
            "CELERY_RESULT_BACKEND", "redis://localhost:6379/1"
        ),
        "task_serializer": "json",
        "accept_content": ["json"],
        "result_serializer": "json",
        "timezone": "UTC",
        "enable_utc": True,
        "task_track_started": True,
        "task_time_limit": 30 * 60,  # 30 minutes
        "task_soft_time_limit": 60,  # 1 minute
        "worker_prefetch_multiplier": 1,
        "worker_max_tasks_per_child": 1000,
        # scheduled beats conf
        "beat_schedule": {
            "send-quiz-reminders-daily": {
                "task": "app.celery_tasks.send_quiz_reminder_emails",
                "schedule": crontab(hour=5, minute=10),
            },
            "monthly-performance-report": {
                "task": "app.celery_tasks.send_monthly_performance_report",
                "schedule": crontab(hour=5, minute=0, day_of_month=1),
            },
        },
        "beat_schedule_filename": "celerybeat-schedule",
    }

    celery = Celery(
        app.import_name,
        broker=celery_config["broker_url"],
        backend=celery_config["result_backend"],
    )

    celery.conf.update(celery_config)

    # Subclass task to run within Flask app context
    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context."""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_app()
CELERY = make_celery(flask_app)
