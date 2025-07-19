from flask import Blueprint, jsonify
from pony import orm

from app.models.database import Subject


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
