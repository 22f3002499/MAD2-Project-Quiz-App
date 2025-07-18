from flask import Flask, g
import os
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS
from celery import Celery


from app.cache import app_cache
from app.mail_service import mail


ENV_FILE = find_dotenv(r".env")
load_dotenv(ENV_FILE)


CELERY = None


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


def create_app():
    global CELERY
    app = Flask(__name__, instance_relative_config=True)
    app_config = {
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "DEBUG": os.environ.get("DEBUG"),
        "JWT_SECRET_KEY": os.environ.get("JWT_SECRET_KEY"),
        "JWT_ACCESS_TOKEN_EXPIRES": os.environ.get("JWT_ACCESS_TOKEN_EXPIRES"),
        "JWT_REFRESH_TOKEN_EXPIRES": os.environ.get("JWT_REFRESH_TOKEN_EXPIRES"),
        # redis config
        "CACHE_TYPE": "RedisCache",
        "CACHE_DEFAULT_TIMEOUT": 300,
        "CACHE_REDIS_HOST": "localhost",
        "CACHE_REDIS_PORT": 6379,
        "CACHE_REDIS_DB": 0,
        # mail config
        "MAIL_SERVER": os.environ.get("MAIL_SERVER"),
        "MAIL_DEBUG": 1,
        "MAIL_PORT": os.environ.get("MAIL_PORT"),
        "MAIL_USE_TLS": True,
        "MAIL_USERNAME": os.environ.get("MAIL_USERNAME"),
        "MAIL_PASSWORD": os.environ.get("MAIL_PASSWORD"),
        "MAIL_DEFAULT_SENDER": os.environ.get("MAIL_USERNAME"),
        # celery config
    }
    app.config.from_mapping(app_config)

    from app.routes.auth import auth_blueprint
    from app.routes.user_routes import user_blueprint
    from app.routes.admin_routes import admin_blueprint
    from app.routes.other_routes import other_routes_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(other_routes_blueprint)

    CORS(
        app,
        origins=["http://localhost:3000", "http://localhost:5173"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
    )

    app_cache.init_app(app)
    mail.init_app(app)
    CELERY = make_celery(app)

    return app
