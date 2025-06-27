from flask import Blueprint, request, g, jsonify
from datetime import datetime
from pony import orm
from marshmallow import ValidationError

from app.models.database import (
    Quiz,
    QuizAttempt,
    Question,
    Option,
    UserAnswer,
    User,
    Subject,
    Chapter,
)
from app.routes.exceptions import (
    APIException,
    QuizAttemptException,
    ResourceNotFoundException,
    QuizException,
    AuthenticationException,
    ResourceException,
)
from app.utils import (
    get_token_from_header,
    get_user_by_token,
)

admin_blueprint = Blueprint("admin_blueprint", __name__, url_prefix="/admin")


@admin_blueprint.before_request
def verify_jwt_token():
    if request.method == "OPTIONS":
        return
    token = get_token_from_header(dict(request.headers))
    user = get_user_by_token(token)
    if user.is_admin == False:
        raise AuthenticationException(message="missing admin role")

    g.current_user: User = user

    return None


@admin_blueprint.get("/home/", defaults={"page_num": 1})
@admin_blueprint.get("/home/<int:page_num>/")
@orm.db_session
def admin_home(page_num):
    results = []
    recent_quiz = orm.select(quiz for quiz in Quiz if not quiz.is_deleted).sort_by(
        Quiz.start_datetime
    )
    recent_quiz = recent_quiz.page(page_num)

    for quiz in recent_quiz:
        quiz_data = {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "duration": quiz.duration,
            "start_datetime": quiz.start_datetime,
            "total_questions": quiz.total_questions,
            "total_marks": quiz.total_marks,
            "subject_title": quiz.subject.title,  # Access the subject title
        }
        results.append(quiz_data)

    return jsonify(results), 200


@admin_blueprint.get("/chapters/<int:subject_id>/")
@orm.db_session
def get_chapters(subject_id: int):
    results = []

    all_chapters = orm.select(
        chap
        for chap in Chapter
        if chap.subject.id == subject_id and not chap.is_deleted
    )

    for chap in all_chapters:
        chap_data = {
            "id": chap.id,
            "title": chap.title,
            "description": chap.description,
        }
        results.append(chap_data)

    return jsonify(results), 200


# assumes correct data is being sent from frontend
@admin_blueprint.post("/create/<string:resource>/")
@orm.db_session
def create_resource(resource: str):
    data = request.get_json()

    if resource == "quiz":
        subject_id = (
            data.get("subject") or data.get("subject_ids") or data.get("subjectIds")
        )
        quiz_data = {k: data[k] for k in data if "subject" not in k}
        quiz_data["subject"] = Subject.get(id=subject_id)
        new_quiz = Quiz(**quiz_data)
        orm.flush()

    elif resource == "chapter":
        subject_id = request.args.get("subject_id")
        if not Subject.exists(id=subject_id):
            raise ResourceNotFoundException()

        sub = Subject.get(id=subject_id)
        new_chapter = Chapter(
            title=data.get("title"), description=data.get("description"), subject=sub
        )
        orm.flush()

    return jsonify(f"new {resource} created"), 201


# assumes that only data which is to be updated is sent from frontend , no null values
@admin_blueprint.put("/edit/<string:resource>/<int:id>/")
@orm.db_session
def edit_resource(resource: str, id: int):
    data = request.get_json()

    if resource == "quiz":
        subject_found = False
        quiz = Quiz.get(id=id)
        for key in data.keys():
            if "subject" in key:
                subject_found = True
                quiz.subject = Subject.get(id=data[key])

        if not subject_found:
            quiz.set(**data)

    elif resource == "chapter":
        chapter_id = request.args.get("chapter_id")

        if not Chapter.exists(id=chapter_id):
            raise ResourceNotFoundException()

        chapter = Chapter.get(id=chapter_id)
        chapter.set(**data)

    return jsonify({"message": f"made changes to {resource}"}), 200


# sends a pair of dicts ; quiz_info and quiz_stats as list
@admin_blueprint.get("/stats/quiz/<int:quiz_id>/")
@orm.db_session
def stats(quiz_id: int):
    quiz: Quiz = Quiz.get(id=quiz_id)

    quiz_info = {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "duration": quiz.duration,
        "start_datetime": quiz.start_datetime,
        "total_questions": quiz.total_questions,
        "total_marks": quiz.total_marks,
        "attempts_allowed": quiz.attempts_allowed,
        "subject_title": quiz.subject.title,  # Access the subject title
    }

    active_quiz_attempts = orm.select(
        qa for qa in QuizAttempt if qa.quiz == quiz and not qa.is_deleted
    )
    quiz_stats = {
        "total_attempts": orm.count(active_quiz_attempts) or 0,
        "unique_users_attempted": orm.distinct(qa.user for qa in active_quiz_attempts)
        or 0,
        "average_score": orm.avg(qa.score for qa in active_quiz_attempts),
        "average_percentage_score": orm.avg(
            qa.percentage_score for qa in active_quiz_attempts
        )
        or 0,
        "highest_score": orm.max(qa.score for qa in active_quiz_attempts) or 0,
        "lowest_score": orm.min(qa.score for qa in active_quiz_attempts) or 0,
        "pass_rate": orm.count(
            qa.percentage_score
            for qa in active_quiz_attempts
            if qa.score > qa.quiz.passing_percentage
        ),
    }

    return jsonify(quiz_info, quiz_stats), 200
