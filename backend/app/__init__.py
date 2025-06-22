from flask import Flask, g
import os
from dotenv import load_dotenv, find_dotenv
from flask_cors import CORS


ENV_FILE = find_dotenv(r".env")
load_dotenv(ENV_FILE)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app_config = {
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "DEBUG": os.environ.get("DEBUG"),
        "JWT_SECRET_KEY": os.environ.get("JWT_SECRET_KEY"),
        "JWT_ACCESS_TOKEN_EXPIRES": os.environ.get("JWT_ACCESS_TOKEN_EXPIRES"),
        "JWT_REFRESH_TOKEN_EXPIRES": os.environ.get("JWT_REFRESH_TOKEN_EXPIRES"),
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
    return app
