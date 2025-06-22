from pony import orm
import pytest

from app.models.database import User
from pony.orm import select


@pytest.fixture()
@orm.db_session
def user_auth_token(client):
    response = client.post(
        "/auth/login/",
        json={
            "username": select(user for user in User if not user.is_admin)[:][
                1
            ].username,
            "password": "password123",
        },
    )
    return str(response.json)


# @orm.db_session
# def test_home(client, user_auth_token):
#     response = client.get(
#         "/user/home/", headers={"Authorization": f"Bearer {user_auth_token}"}
#     )
#     assert response.status_code == 200


@orm.db_session
def test_scores(client, user_auth_token):
    response = client.get(
        "/user/scores/", headers={"Authorization": f"Bearer {user_auth_token}"}
    )
    assert response.status_code == 200
