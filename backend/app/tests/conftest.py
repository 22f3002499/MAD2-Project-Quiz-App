import pytest
from app import create_app
from .gen_fake_data import generate_fake_data


@pytest.fixture(scope="session")
def app():
    app = create_app()

    with app.app_context():
        generate_fake_data()

    app.config.update({"TESTING": True})
    yield app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


# @pytest.fixture()
# def auth_token():
#     auth_url = "localhost"
