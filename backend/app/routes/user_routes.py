from flask import Blueprint, request, g, jsonify, make_response
from datetime import datetime
from pony import orm
import json

from app.models.database import (
    Quiz,
    QuizAttempt,
    Question,
    Option,
    UserAnswer,
    User,
    Chapter,
    Subject,
)
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

from app.cache import app_cache

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/user")


@user_blueprint.before_request
# @db_session
def verify_jwt_token():
    if request.method == "OPTIONS":
        return
    token = get_token_from_header(dict(request.headers))
    user = get_user_by_token(token)

    if user.is_admin:
        return jsonify({"message": "admins arent allowed on user routes"}), 400

    if user.is_deleted or user.is_banned:
        return jsonify({"message": "invalid user"}), 400
    else:
        g.current_user: User = user


@user_blueprint.get("/quiz/")
@app_cache.cached(key_prefix="user_quiz")
@orm.db_session
def user_quiz():
    results = []
    user_subjects = orm.select(
        sub for sub in g.current_user.subjects if not sub.is_deleted
    )
    user_chapters = orm.select(
        chap for chap in Chapter if chap.subject in user_subjects
    )
    user_quizzes = orm.select(
        quiz
        for quiz in Quiz
        if (quiz.chapter in user_chapters) and quiz.start_datetime > datetime.now()
    ).sort_by(Quiz.start_datetime)
    print(user_chapters[:], user_quizzes[:])

    for quiz in user_quizzes:
        quiz_data = {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "duration": quiz.duration,
            "start_datetime": quiz.start_datetime.timestamp(),
            "total_questions": quiz.total_questions,
            "total_marks": quiz.total_marks,
            "chapter_title": quiz.chapter.title,
            "subject_title": quiz.chapter.subject.title,  # Access the subject title
        }
        results.append(quiz_data)

    return jsonify(results), 200


@user_blueprint.get("/scores/")
@app_cache.cached(key_prefix="user_scores")
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
            "subject_title": quiz_attempt.quiz.chapter.subject.title,
            "chapter_title": quiz_attempt.quiz.chapter.title,
            "quiz_total_marks": quiz_attempt.quiz.total_marks,
            "score": quiz_attempt.score,
            "passing_percentage": quiz_attempt.quiz.passing_percentage,
            "percentage_score": quiz_attempt.percentage_score,
            "submit_datetime": quiz_attempt.submit_datetime.timestamp(),
        }
        results.append(quiz_attempt_data)

    return jsonify(results), 200


# PENDING
@user_blueprint.get("/review-answers/<int:quiz_attempt_id>/")
@app_cache.cached(key_prefix="user_review_answers")
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
            "image": ques.image,
            "type": ques.type,
            "marks": ques.marks,
            "options": [],
        }

        for option in ques_options:
            option_data = {
                "id": option.id,
                "title": option.title,
                "description": option.description,
                "image": option.image,
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
            "image": ques.image,
            "type": ques.type,
            "options": [],
        }

        for option in ques.options:
            option_data = {
                "id": option.id,
                "title": option.title,
                "description": option.description,
                "image": option.image,
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
@app_cache.cached(key_prefix="user_stats")
@orm.db_session
def user_stats():
    quiz_attempts = orm.select(
        qa for qa in QuizAttempt if qa.user == g.current_user and not qa.is_deleted
    )

    if not quiz_attempts[:]:
        return jsonify(
            {
                "total_attempts": 0,
                "average_score": 0,
                "pass_rate": 0,
                "total_subjects": 0,
                "recent_attempts": [],
                "subject_wise_stats": [],
            }
        )

    total_attempts = len(quiz_attempts)
    total_score = orm.sum(qa.score for qa in quiz_attempts)
    average_score = round(total_score / total_attempts, 2)

    passed_attempts = orm.count(
        qa for qa in quiz_attempts if qa.percentage_score >= qa.quiz.passing_percentage
    )
    pass_rate = round((passed_attempts / total_attempts) * 100, 2)

    # Subject-wise statistics
    subject_stats = {}
    for attempt in quiz_attempts:
        subject = attempt.quiz.chapter.subject
        subject_name = subject.title

        if subject_name not in subject_stats:
            subject_stats[subject_name] = {
                "subject_name": subject_name,
                "attempts": 0,
                "total_score": 0,
                "passed": 0,
            }

        subject_stats[subject_name]["attempts"] += 1
        subject_stats[subject_name]["total_score"] += attempt.score
        if attempt.percentage_score >= attempt.quiz.passing_percentage:
            subject_stats[subject_name]["passed"] += 1

    # Calculate averages and pass rates for subjects
    subject_wise_stats = []
    for subject_name, stats in subject_stats.items():
        avg_score = round(stats["total_score"] / stats["attempts"], 2)
        subject_pass_rate = round((stats["passed"] / stats["attempts"]) * 100, 2)

        subject_wise_stats.append(
            {
                "subject_name": subject_name,
                "attempts": stats["attempts"],
                "average_score": avg_score,
                "pass_rate": subject_pass_rate,
            }
        )

    # Sort by number of attempts (descending)
    subject_wise_stats.sort(key=lambda x: x["attempts"], reverse=True)

    # Recent attempts (last 5)
    recent_attempts_query = (
        orm.select(
            qa for qa in QuizAttempt if qa.user == g.current_user and not qa.is_deleted
        )
        .order_by(orm.desc(QuizAttempt.submit_datetime))
        .limit(5)
    )

    recent_attempts = []
    for attempt in recent_attempts_query:
        recent_attempts.append(
            {
                "quiz_title": attempt.quiz.title,
                "subject": attempt.quiz.chapter.subject.title,
                "score": round(attempt.score, 2),
                "total_marks": attempt.quiz.total_marks,
                "percentage": round(attempt.percentage_score, 2),
                "passed": attempt.percentage_score >= attempt.quiz.passing_percentage,
                "date": attempt.submit_datetime.strftime("%Y-%m-%d %H:%M"),
            }
        )

    return jsonify(
        {
            "total_attempts": total_attempts,
            "average_score": average_score,
            "pass_rate": pass_rate,
            "total_subjects": len(subject_wise_stats),
            "recent_attempts": recent_attempts,
            "subject_wise_stats": subject_wise_stats,
        }
    )


@user_blueprint.get("/monthly-report/")
def trigger_monthly_report():
    from app.celery_tasks import send_monthly_csv_report

    current_user_id = g.current_user.id
    send_monthly_csv_report(current_user_id)
    return jsonify({"message": "You will recieve the report shortly"})


# ERROR HANDLING
@user_blueprint.errorhandler(TypeError)
def handle_typerror(e):
    return jsonify(str(e)), 400


@user_blueprint.errorhandler(APIException)
def handle_auth_error(e: APIException):
    return jsonify(e.to_dict()), e.status_code
