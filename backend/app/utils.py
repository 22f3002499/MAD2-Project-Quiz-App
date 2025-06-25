from flask import current_app
from jwt import encode, decode, DecodeError, InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta
from pony.orm import select, db_session

from app.routes.exceptions import (
    AuthenticationException,
    ResourceNotFoundException,
    JWTTokenException,
    QuizAttemptException,
)
from app.models.database import User


def generate_jwt_token(payload: dict) -> str:
    # FIX IN PROD
    exp_time = (
        timedelta(seconds=int(current_app.config["JWT_ACCESS_TOKEN_EXPIRES"] or 3600))
        + datetime.utcnow()
    )
    payload["exp"] = exp_time
    payload["iat"] = datetime.utcnow()

    return encode(payload=payload, key=current_app.config["JWT_SECRET_KEY"])


def refresh_jwt_token(old_token: str) -> str:
    try:
        payload = decode(
            old_token, key=current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
    except (InvalidTokenError, DecodeError, ExpiredSignatureError) as error:
        raise AuthenticationException(
            message="Invalid or expired token",
            status_code=400,
            payload={"root_error": str(error)},
        )

    exp_time = (
        timedelta(seconds=int(current_app.config["JWT_REFRESH_TOKEN_EXPIRES"] or 43200))
        + datetime.utcnow()
    )
    payload["exp"] = exp_time
    payload["iat"] = datetime.utcnow()

    return encode(payload=payload, key=current_app.config["JWT_SECRET_KEY"])


@db_session
def get_user_by_token(token: str) -> User:
    try:
        token_data = decode(
            token, key=current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
    except (InvalidTokenError, DecodeError, ExpiredSignatureError) as error:
        raise AuthenticationException(
            message="Invalid or expired token", status_code=400, payload=error
        )

    try:
        user = select(
            user
            for user in User
            if user.username == token_data["username"]
            and user.id == int(token_data["user_id"])
            and not user.is_deleted
        ).first()
    except IndexError:
        raise ResourceNotFoundException("user not found")

    return user


def get_token_from_header(request_headers: dict) -> str:
    data = request_headers.get("Authorization")
    if not data:
        raise AuthenticationException("jwt token not found")
    if "Bearer" not in data:
        raise JWTTokenException()

    try:
        token = str(data).split(" ")[1]
    except IndexError:
        raise JWTTokenException("jwt token not found in authorization headers")

    return token
