from werkzeug.security import generate_password_hash, check_password_hash
from pony import orm
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from datetime import datetime

from app.models.database import User, Subject
from app.routes.exceptions import APIException, AuthenticationException
from app.utils import refresh_jwt_token, generate_jwt_token, get_token_from_header

auth_blueprint = Blueprint(
    name="auth_blueprint", import_name=__name__, url_prefix="/auth"
)


@auth_blueprint.post("/register/")
@orm.db_session
def register_user():
    data = request.get_json()

    user = User(
        email=data.get("email"),
        username=data.get("username"),
        password=data.get("password"),
        date_of_birth=data.get("dob", None),
    )
    orm.flush()
    subject_ids = (
        data.get("subject_id", [])
        or data.get("subjects", [])
        or data.get("subject_ids", [])
    )
    for subject_id in subject_ids:
        user.subjects.add(Subject.get(id=subject_id))

    return jsonify({"message": "User created"}), 201


@auth_blueprint.post("/login/")
@orm.db_session
def login_user():
    login_data = request.get_json()

    user = orm.select(
        user
        for user in User
        if user.username == login_data["username"] and not user.is_deleted
    ).first()

    if not user or not check_password_hash(user.password, login_data["password"]):
        raise AuthenticationException("Incorrect username or password")

    user.last_login = datetime.now()
    token = generate_jwt_token(
        {
            "user_id": user.id,
            "username": user.username,
            "role": "admin" if user.is_admin else "user",
        }
    )

    return jsonify(token), 200


@auth_blueprint.get("/refresh-token/")
def refresh_token():
    token = get_token_from_header(dict(request.headers))
    new_token = refresh_jwt_token(token)

    return jsonify(new_token), 200


# ERROR HANDLING


@auth_blueprint.errorhandler(TypeError)
def handle_typerror(e):
    return jsonify(str(e)), 400


@auth_blueprint.errorhandler(APIException)
def handle_auth_error(e: APIException):
    print(e.to_dict())
    return jsonify(e.to_dict()), e.status_code
