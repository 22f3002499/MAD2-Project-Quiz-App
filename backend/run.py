from app import create_app
from app.models.database import init_db
from app import CELERY


def main():
    app = create_app()

    # Tables are only created if they do not exist
    with app.app_context():
        init_db()

    app.run(port=5000, debug=eval(app.config["DEBUG"]))


if __name__ == "__main__":
    main()
