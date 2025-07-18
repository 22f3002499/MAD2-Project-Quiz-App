from flask import Blueprint, request, g, jsonify
from pony import orm
from flask_mail import Message

from app.models.database import Subject
from app.mail_service import mail, send_reminder_mail

other_routes_blueprint = Blueprint(
    "other_routes_blueprint", __name__, url_prefix="/other"
)


@other_routes_blueprint.get("/subject/")
@orm.db_session
def get_subjects():
    all_subjects = orm.select(sub for sub in Subject if not sub.is_deleted)
    result = [
        {"id": sub.id, "title": sub.title, "description": sub.description}
        for sub in all_subjects
    ]

    return jsonify(result), 200


@other_routes_blueprint.get("/send/")
def send_test_mail():
    user_data = {"email": "tejasvgamer33@gmail.com", "username": "sodies"}
    quiz_data = {
        "title": "Quizzz",
        "subject": "SUBJECT",
        "description": "THISDHFDSJLFDSJFJSD",
    }

    send_reminder_mail(user_data, quiz_data)
