from pony import orm
import pytest

from app.models.database import User


@pytest.fixture()
@orm.db_session
def admin_auth_token(client):
    response = client.post(
        "/auth/login/",
        json={
            "username": orm.select(user for user in User if user.is_admin)[:][
                0
            ].username,
            "password": "password123",
        },
    )
    return str(response.json)


@orm.db_session
def test_home(client, admin_auth_token):
    response = client.get(
        "/admin/home/2/",
        headers={"Authorization": f"Bearer {admin_auth_token}"},
    )
    assert response.status_code == 200
