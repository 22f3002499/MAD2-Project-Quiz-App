from flask import Blueprint, request, g, jsonify
from datetime import datetime, timedelta
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


@admin_blueprint.get("/dashboard/")
@orm.db_session
def get_dashboard_stats():

    stats = {
        "total_users": orm.count(
            user for user in User if not user.is_deleted and not user.is_admin
        ),
        "total_quizzes": orm.count(quiz for quiz in Quiz if not quiz.is_deleted),
        "total_quiz_attempts": orm.count(qa for qa in QuizAttempt if not qa.is_deleted),
        "total_subjects": orm.count(sub for sub in Subject if not sub.is_deleted),
        "average_quiz_score": orm.avg(
            qa.percentage_score for qa in QuizAttempt if not qa.is_deleted
        )
        * 100,
        "active_users_today": orm.count(
            user
            for user in User
            if user.last_login.date() == datetime.now().date()
            and not user.is_deleted
            and not user.is_admin
        ),
        "average_pass_rate": (
            orm.count(
                qa
                for qa in QuizAttempt
                if not qa.is_deleted
                and qa.percentage_score >= qa.quiz.passing_percentage
            )
            / orm.count(qa for qa in QuizAttempt if not qa.is_deleted)
        )
        * 100,
    }
    ## PENDING QUIZZES
    quizzes_today = orm.select(
        quiz for quiz in Quiz if quiz.start_datetime == datetime.today()
    )
    pending_quizzes_count = 0
    for quiz in quizzes_today:
        attempt_count = orm.count(
            qa for qa in QuizAttempt if qa.quiz == quiz and not qa.is_deleted
        )
        if attempt_count == 0:
            pending_quizzes_count += 1

    if quizzes_today:
        stats["pending_quizzes_today"] = (
            pending_quizzes_count / len(quizzes_today) * 100
        )
    else:
        stats["pending_quizzes_today"] = 0

    ## TOP PERFORMERS
    performers = []

    users_with_attempts = orm.select(
        qa.user for qa in QuizAttempt if not qa.is_deleted and not qa.user.is_deleted
    ).distinct()

    for user in users_with_attempts:
        user_attempts = orm.select(
            qa for qa in QuizAttempt if qa.user == user and not qa.is_deleted
        )

        total_attempts = orm.count(user_attempts)
        avg_score = orm.avg(qa.percentage_score for qa in user_attempts)

        passed_attempts = orm.count(
            qa
            for qa in user_attempts
            if qa.percentage_score >= qa.quiz.passing_percentage
        )
        pass_rate = (
            (passed_attempts / total_attempts) * 100 if total_attempts > 0 else 0
        )
        unique_quizzes = orm.count(
            orm.select(qa.quiz for qa in user_attempts).distinct()
        )

        performer_data = {
            "id": user.id,
            "username": user.username,
            "average_percentage_score": round(avg_score, 2),
            "pass_rate": round(pass_rate, 2),
            "unique_quizzes_attempted": unique_quizzes,
        }

        performers.append(performer_data)

    performers.sort(key=lambda x: x["average_percentage_score"], reverse=True)

    for i, performer in enumerate(performers):
        performer["rank"] = i + 1

    stats["top_performers"] = performers[:50]

    ## SUBJECT STATS

    subject_stats = []

    subjects = orm.select(s for s in Subject if not s.is_deleted).order_by(
        Subject.title
    )

    for subject in subjects:
        quizzes = orm.select(
            q
            for c in subject.chapters
            for q in c.quizzes
            if not c.is_deleted and not q.is_deleted
        )

        total_quizzes = orm.count(quizzes)

        quiz_attempts = orm.select(
            qa
            for c in subject.chapters
            for q in c.quizzes
            for qa in q.quiz_attempts
            if not c.is_deleted and not q.is_deleted and not qa.is_deleted
        )

        attempts_list = list(quiz_attempts)
        if attempts_list:
            average_percentage_score = round(
                sum(qa.percentage_score for qa in attempts_list) / len(attempts_list), 2
            )

            passed_attempts = sum(
                1
                for qa in attempts_list
                if qa.percentage_score >= qa.quiz.passing_percentage
            )
            pass_rate = round((passed_attempts * 100.0) / len(attempts_list), 2)
        else:
            average_percentage_score = 0
            pass_rate = 0

        subject_stats.append(
            {
                "subject_name": subject.title,
                "total_quizzes": total_quizzes,
                "average_percentage_score": average_percentage_score,
                "pass_rate": pass_rate,
            }
        )

    stats["subject_performance"] = subject_stats

    return jsonify(stats), 200


@admin_blueprint.errorhandler(AttributeError)
def handle_attribute_error(e: AttributeError):
    return jsonify(str(e)), 404


@admin_blueprint.errorhandler(APIException)
def handle_auth_error(e: APIException):
    return jsonify(e.to_dict()), e.status_code


# @admin_blueprint.errorhandler(orm.RowNotFound)
# def handle_row_not_found(e):
#     return jsonify(e), 404
