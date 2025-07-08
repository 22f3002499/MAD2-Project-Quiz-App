from flask import Blueprint, request, g, jsonify
from datetime import datetime
from pony import orm

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


@admin_blueprint.get("/quizzes/")
@orm.db_session
def get_quizzes():
    results = []
    recent_quiz = orm.select(quiz for quiz in Quiz if not quiz.is_deleted).sort_by(
        Quiz.start_datetime
    )

    for quiz in recent_quiz:
        quiz_data = {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "duration": quiz.duration,
            "start_datetime": quiz.start_datetime.timestamp(),
            "total_questions": quiz.total_questions,
            "total_marks": quiz.total_marks,
            "attempts_allowed": quiz.attempts_allowed,
            "passing_percentage": quiz.passing_percentage,
            "chapter": quiz.chapter.to_dict(only=["id", "title", "description"]),
            "subject": quiz.chapter.subject.to_dict(
                only=["id", "title", "description"]
            ),
        }
        results.append(quiz_data)

    return jsonify(results), 200


@admin_blueprint.get("/quiz/questions-and-options/<int:quiz_id>/")
@orm.db_session
def get_quiz_questions_and_options(quiz_id: int):
    results = []

    quiz = Quiz.get(id=quiz_id)
    quiz_questions = orm.select(ques for ques in quiz.questions if not ques.is_deleted)

    for ques in quiz_questions:
        ques_data = {
            "id": ques.id,
            "title": ques.title,
            "description": ques.description,
            "image": ques.image,
            "marks": ques.marks,
            "type": ques.type,
        }
        ques_data["options"] = []

        for opt in ques.options:
            if opt.is_deleted:
                continue

            opt_data = {
                "id": opt.id,
                "title": opt.title,
                "description": opt.description,
                "image": opt.image,
                "is_correct": opt.is_correct,
            }
            ques_data["options"].append(opt_data)

        results.append(ques_data)

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
    has_files = bool(request.files)

    if has_files:
        data = dict(request.form)
    else:
        data = request.get_json()

    if resource == "quiz":
        new_data = {k: v for k, v in data.items() if k not in ["chapter", "subject"]}

        new_data["chapter"] = Chapter.get(id=data.get("chapter"))
        new_quiz = Quiz(**new_data)
        orm.flush()

    elif resource == "subject":
        new_subject = Subject(
            title=data.get("title"),
            description=data.get("description"),
        )
        orm.flush()
        new_subject.user.add(User.get(id=g.current_user.id))

    elif resource == "chapter":
        subject_id = request.args.get("subject_id")
        if not Subject.exists(id=subject_id):
            raise ResourceNotFoundException(f"Subject with id: {subject_id} not found")

        sub = Subject.get(id=subject_id)
        new_chapter = Chapter(
            title=data.get("title"), description=data.get("description"), subject=sub
        )
        orm.flush()

    elif resource == "question":
        quiz_id = request.args.get("quiz_id")
        if not Quiz.exists(id=quiz_id):
            raise ResourceNotFoundException(f"Quiz with id: {id} not found")

        quiz = Quiz.get(id=quiz_id)

        if "_image" in request.files:
            image_file = request.files["_image"]
            if image_file and image_file.filename:
                data["_image"] = image_file.read()
            elif image_file.filename == "":
                data["_image"] = None

        new_question = Question(
            title=data.get("title"),
            description=data.get("description"),
            _image=data.get("_image"),
            marks=data.get("marks"),
            quiz=quiz,
        )
        orm.flush()

    elif resource == "option":
        question_id = request.args.get("question_id")

        if not Question.exists(id=question_id):
            raise ResourceNotFoundException(
                f"Question with id: {question_id} not found"
            )

        ques = Question.get(id=question_id)

        if "_image" in request.files:
            image_file = request.files["_image"]
            if image_file and image_file.filename:
                data["_image"] = image_file.read()
            elif image_file.filename == "":
                data["_image"] = None

        new_option = Option(
            title=data.get("title"),
            description=data.get("description"),
            _image=data.get("_image"),
            is_correct=data.get("is_correct"),
            question=ques,
        )
        orm.flush()

    return jsonify(f"new {resource} created"), 201


# assumes that only data which is to be updated is sent from frontend , no null values
@admin_blueprint.put("/edit/<string:resource>/<int:id>/")
@orm.db_session
def edit_resource(resource: str, id: int):
    has_files = bool(request.files)

    if has_files:
        data = dict(request.form)
    else:
        data = request.get_json()

    if resource == "chapter":
        if not Chapter.exists(id=id):
            raise ResourceNotFoundException(f"Chapter with id: {id} not found")

        chapter = Chapter.get(id=id)
        chapter.set(**data)

    elif resource == "subject":
        if not Subject.exists(id=id):
            raise ResourceNotFoundException(f"Subject with id: {id} not found")

        subject = Subject.get(id=id)
        subject.set(**data)

    elif resource == "quiz":
        if not Quiz.exists(id=id):
            raise ResourceNotFoundException(f"Quiz with id: {id} not found")
        if not Chapter.exists(id=data["chapter"]):
            raise ResourceNotFoundException(
                f"Chapter with id: {id} for the quiz not found"
            )

        quiz = Quiz.get(id=id)
        new_data = {k: v for k, v in data.items() if k not in ["chapter", "subject"]}
        new_data["chapter"] = Chapter.get(id=data.get("chapter"))

        quiz.set(**new_data)

    elif resource == "question":
        if not Question.exists(id=id):
            raise ResourceNotFoundException(f"Question with id: {id} not found")

        if "_image" in request.files:
            image_file = request.files["_image"]
            if image_file and image_file.filename:
                data["_image"] = image_file.read()
            elif image_file.filename == "":
                data["_image"] = None

        question = Question.get(id=id)

        question.set(**data)

    elif resource == "option":
        if not Option.exists(id=id):
            raise ResourceNotFoundException(f"Option with id: {id} not found")

        if "_image" in request.files:
            image_file = request.files["_image"]
            if image_file and image_file.filename:
                data["_image"] = image_file.read()
            elif image_file.filename == "":
                data["_image"] = None

        option = Option.get(id=id)

        option.set(**data)

    return jsonify({"message": f"Changed {resource}"}), 200


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


@admin_blueprint.get("/test/<int:id>")
@orm.db_session
def testing_route(id: int):
    return jsonify("yayy"), 200


@admin_blueprint.errorhandler(AttributeError)
def handle_attribute_error(e: AttributeError):
    return jsonify(str(e)), 404


# @admin_blueprint.errorhandler(APIException)
# def handle_auth_error(e: APIException):
#     return jsonify(e.to_dict()), e.status_code


# @admin_blueprint.errorhandler(orm.RowNotFound)
# def handle_row_not_found(e):
#     return jsonify(e), 404
