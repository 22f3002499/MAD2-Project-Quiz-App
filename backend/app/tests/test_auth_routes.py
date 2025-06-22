from pony import orm
import pytest
from datetime import datetime

from app.models.database import User, Subject


@pytest.fixture()
@orm.db_session
def user_auth_token(client):
    response = client.post(
        "/auth/login/", json={"username": User[1].username, "password": "password123"}
    )
    return str(response.json)


@orm.db_session
def test_login(client):
    response = client.post(
        "/auth/login/", json={"username": User[1].username, "password": "password123"}
    )
    assert response.status_code == 200


@orm.db_session
def test_register(client):

    # send the first 3 subjects
    subjects = orm.select(sub.id for sub in Subject if sub.id < 3)[:]
    user_data = {
        "email": "sodies@email.com",
        "password": "password123",
        "username": "sodies",
        "date_of_birth": datetime.date(datetime.now()).isoformat(),
        "subject_id": list(subjects),
    }
    response = client.post(
        "/auth/register/",
        json=user_data,
    )
    assert (
        User.exists(username=user_data["username"], email=user_data["email"])
        and response.status_code == 201
    )


def test_refresh_token(client, user_auth_token):
    response = client.get(
        "/auth/refresh-token/", headers={"Authorization": f"Bearer {user_auth_token}"}
    )
    assert response.status_code == 200
