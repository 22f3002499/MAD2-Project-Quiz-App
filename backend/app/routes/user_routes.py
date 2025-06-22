from flask import Blueprint, request, g, jsonify, make_response
from datetime import datetime
from pony import orm
from marshmallow import ValidationError
import json

from app.models.database import Quiz, QuizAttempt, Question, Option, UserAnswer, User
from app.routes.exceptions import (
    APIException,
    QuizAttemptException,
    ResourceNotFoundException,
    QuizException,
)
from app.utils import (
    get_token_from_header,
    get_user_by_token,
)

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/user")


@user_blueprint.before_request
# @db_session
def verify_jwt_token():
    if request.method == "OPTIONS":
        return
    token = get_token_from_header(dict(request.headers))
    user = get_user_by_token(token)

    if user.is_deleted or user.is_banned:
        return jsonify({"message": "invalid credentials"}), 400
    else:
        g.current_user: User = user


@user_blueprint.get("/quiz/")
@orm.db_session
def user_quiz():
    results = []
    user_subjects = orm.select(sub for sub in g.current_user.subjects)
    all_quiz = orm.select(
        q for q in Quiz if not q.is_deleted and q.subject in user_subjects
    )

    for quiz in all_quiz:
        quiz_data = {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "duration": quiz.duration,
            "start_datetime": quiz.start_datetime.timestamp(),
            "total_questions": quiz.total_questions,
            "total_marks": quiz.total_marks,
            "subject_title": quiz.subject.title,  # Access the subject title
        }
        results.append(quiz_data)

    return jsonify(results), 200


@user_blueprint.get("/scores/")
@orm.db_session
def user_scores():

    results = []
    all_quiz_attempts = orm.select(
        qa for qa in QuizAttempt if not qa.is_deleted and qa.user == g.current_user
    ).order_by(QuizAttempt.submit_datetime)

    for quiz_attempt in all_quiz_attempts:
        quiz_attempt_data = {
            "id": quiz_attempt.id,
            "quiz_title": quiz_attempt.quiz.title,
            "subject_title": quiz_attempt.quiz.subject.title,
            "quiz_total_marks": quiz_attempt.quiz.total_marks,
            "score": quiz_attempt.score,
            "percentage_score": quiz_attempt.percentage_score,
            "submit_datetime": quiz_attempt.submit_datetime.timestamp(),
        }
        results.append(quiz_attempt_data)

    return jsonify(results), 200


# PENDING
@user_blueprint.get("/review-answers/<int:quiz_attempt_id>/")
@orm.db_session
def review_answers(quiz_attempt_id: int):
    if not QuizAttempt.exists(id=quiz_attempt_id):
        raise ResourceNotFoundException(
            f"QuizAttempt with id:{quiz_attempt_id} not found"
        )

    quiz_attempt = QuizAttempt.get(id=quiz_attempt_id)

    if quiz_attempt.is_deleted:
        raise ResourceNotFoundException(
            f"QuizAttempt with id:{quiz_attempt_id} not found"
        )

    quiz_questions = orm.select(
        ques for ques in quiz_attempt.quiz.questions if not ques.is_deleted
    )
    results = []

    for ques in quiz_questions:
        ques_options = orm.select(opt for opt in ques.options if not opt.is_deleted)
        user_selected_options = (
            orm.select(
                ua
                for ua in UserAnswer
                if ua.quiz_attempt == quiz_attempt and ua.question == ques
            )
            .first()
            .options
        )
        ques_data = {
            "id": ques.id,
            "title": ques.title,
            "description": ques.description,
            "image": ques.get_encoded_image(),
            "type": ques.get_type(),
            "marks": ques.marks,
            "options": [],
        }

        for option in ques_options:
            option_data = {
                "id": option.id,
                "title": option.title,
                "description": option.description,
                "image": option.get_encoded_image(),
                "is_correct": option.is_correct,
            }
            ques_data["options"] += [option_data]

        ques_data["user_selected_options"] = [opt.id for opt in user_selected_options]

        results.append(ques_data)

    # HANDLE DOWNLOAD
    if request.args.get("download") == "true":
        json_string = json.dumps(results, ensure_ascii=False, indent=2)
        response = make_response(json_string)
        response.headers["Content-Type"] = "application/json"
        response.headers["Content-Disposition"] = (
            f"attachment; filename=review-answers-{quiz_attempt.quiz.id}-{quiz_attempt.id}.json"
        )

        print(response)
        return response

    return jsonify(results), 200


@user_blueprint.get("/start-quiz/<int:quiz_id>/")
@orm.db_session
def user_start_quiz(quiz_id: int):
    if not Quiz.exists(id=quiz_id):
        raise ResourceNotFoundException(f"Quiz with id:{quiz_id} not found.")

    quiz = Quiz.get(id=quiz_id)
    if (
        orm.select(
            qa
            for qa in QuizAttempt
            if qa.quiz == quiz and not qa.is_deleted and qa.user == g.current_user
        ).count()
        >= quiz.attempts_allowed
    ):
        raise QuizAttemptException("Quiz already attempted. No more attempts allowed.")
    # if QuizAttempt.exists(quiz=quiz_id, user=g.current_user.id):

    if quiz.start_datetime > datetime.now():
        raise QuizException("Quiz hasnt started yet.")

    results = []
    all_questions = orm.select(
        q for q in Question if q.quiz.id == quiz_id and not q.is_deleted
    )

    for ques in all_questions:
        ques_data = {
            "id": ques.id,
            "title": ques.title,
            "description": ques.description,
            "image": ques.get_encoded_image(),
            "type": ques.get_type(),
            "options": [],
        }

        for option in ques.options:
            option_data = {
                "id": option.id,
                "title": option.title,
                "description": option.description,
                "image": option.get_encoded_image(),
            }
            ques_data["options"] += [option_data]

        results.append(ques_data)

    return jsonify([results, {"quiz_duration": quiz.duration}]), 200


@user_blueprint.post("/submit-quiz/<int:quiz_id>/")
@orm.db_session
def user_submit_quiz(quiz_id: int):
    """
    expected json: {
        "1" : [2,3,4] ----> For MSQ type
        "2" : [8] ----> For MCQ type
        ques_id : [opt_id , opt_id , opt_id]
    }

    """
    if not Quiz.exists(id=quiz_id):
        raise ResourceNotFoundException(f"Quiz with id:{quiz_id} not found.")

    if Quiz.get(id=quiz_id).start_dateime > datetime.now():
        raise QuizException("Quiz hasnt started yet.")

    data = request.json

    new_quiz_attempt = QuizAttempt(quiz=Quiz.get(id=quiz_id), user=g.current_user)
    orm.flush()

    # calc score before making a new_entry in quiz_attempt
    for ques_id in data:
        ques = Question.get(id=int(ques_id))
        new_user_answer = UserAnswer(quiz_attempt=new_quiz_attempt, question=ques)
        for opt_id in data[ques_id]:
            opt = Option.get(id=opt_id)
            new_user_answer.options.add(opt)

    new_quiz_attempt.calc_score()
    new_quiz_attempt.calc_percentage_score()

    return 201


@user_blueprint.get("/stats/")
def user_stats():
    return None


# ERROR HANDLING
# @user_blueprint.errorhandler(ValidationError)
# def handle_validation_error(e):
#     return jsonify(str(e)), 400


# @user_blueprint.errorhandler(TypeError)
# def handle_typerror(e):
#     return jsonify(str(e)), 400


# @user_blueprint.errorhandler(APIException)
# def handle_auth_error(e: APIException):
#     return jsonify(e.to_dict()), e.status_code
