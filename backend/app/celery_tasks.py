from app import CELERY
from pony import orm
from datetime import datetime, timedelta
import time

from app.mail_service import (
    send_reminder_mail,
    generate_and_send_monthly_report,
    get_quiz_stats_csv,
)
from app.models.database import User, Quiz, Subject, Chapter


@CELERY.task
def send_quiz_reminder_emails():
    tomorrow = datetime.now().date() + timedelta(days=1)
    tomorrow_start = datetime.combine(tomorrow, datetime.min.time())
    tomorrow_end = datetime.combine(tomorrow, datetime.max.time())

    with orm.db_session:
        all_user = orm.select(
            user
            for user in User
            if not user.is_deleted or not user.is_banned or not user.is_admin
        )

        for user in all_user:
            for subject in user.subjects:
                if subject.is_deleted:
                    continue

                for chapter in subject.chapters:
                    if chapter.is_deleted:
                        continue

                    for quiz in chapter.quizzes:
                        if quiz.is_deleted:
                            continue
                        if not (tomorrow_start <= quiz.start_datetime <= tomorrow_end):
                            continue

                        send_reminder_mail(user.to_dict(), quiz.to_dict())
                        time.sleep(1)

    return "Quiz Emails Sent"


@CELERY.task
def send_monthly_performance_report():
    with orm.db_session:
        all_user = orm.select(
            user
            for user in User
            if not user.is_deleted or not user.is_banned or not user.is_admin
        )

        for user in all_user:
            generate_and_send_monthly_report(user)
            time.sleep(1)
    return "MAIL SENT"


@CELERY.task
def send_monthly_csv_report(user_id):
    get_quiz_stats_csv(user_id)
    return "Mails sent"
