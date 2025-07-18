from flask_mail import Mail, Message
from pony import orm
from datetime import datetime, timedelta
from flask import current_app, render_template_string
from calendar import monthrange
import csv
import os

from app.models.database import Quiz, QuizAttempt, User


mail = Mail()


def send_reminder_mail(user_data: dict, quiz_data: dict):

    msg = Message(
        subject="Quiz Reminder",
        recipients=[user_data["email"]],
        html=render_reminder_html_template(user_data["username"], quiz_data),
    )
    mail.send(msg)


def render_reminder_html_template(user_name: str, quiz_data):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background-color: #f9f9f9; }}
            .quiz-card {{ background-color: white; padding: 15px; margin: 15px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            .button {{ background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }}
            .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Daily Quiz Reminder</h1>
            </div>
            <div class="content">
                <h2>Hello {user_name}! You have a quiz on {quiz_data["start_datetime"]}</h2>
                
                <div class="quiz-card">
                    <h3>{quiz_data['title']}</h3>
                    <p><strong>Subject:</strong> {quiz_data['subject']}</p>
                    <p>{quiz_data['description']}</p>
                </div>
                
                <p>Ready to test your knowledge?</p>
            </div>
        </div>
    </body>
    </html>
    """


def generate_and_send_monthly_report(user):
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    first_day = datetime(current_year, current_month, 1)
    last_day_num = monthrange(current_year, current_month)[1]
    last_day = datetime(current_year, current_month, last_day_num, 23, 59, 59)

    with orm.db_session:
        monthly_attempts = []
        for qa in user.quiz_attempts:
            if (
                qa.submit_datetime >= first_day
                and qa.submit_datetime <= last_day
                and not qa.is_deleted
            ):
                monthly_attempts.append(qa)

        total_quizzes = len(monthly_attempts)

        if total_quizzes == 0:
            mail.send_no_activity_report(user, current_month, current_year)
            return

        scores = [attempt.percentage_score for attempt in monthly_attempts]
        average_score = sum(scores) / len(scores)
        highest_score = max(scores)
        lowest_score = min(scores)

        unique_quizzes = set(attempt.quiz.id for attempt in monthly_attempts)
        unique_quiz_count = len(unique_quizzes)

        all_attempts_this_month = []
        for qa in QuizAttempt.select():
            if (
                qa.submit_datetime >= first_day
                and qa.submit_datetime <= last_day
                and not qa.is_deleted
            ):
                all_attempts_this_month.append(qa)

        all_scores = [attempt.percentage_score for attempt in all_attempts_this_month]
        overall_average = sum(all_scores) / len(all_scores) if all_scores else 0

        if average_score >= 90:
            ranking_position = "Top 10%"
        elif average_score >= 80:
            ranking_position = "Top 25%"
        elif average_score > overall_average:
            ranking_position = "Above Average"
        else:
            ranking_position = "Below Average"

        recent_attempts = sorted(
            monthly_attempts, key=lambda x: x.submit_datetime, reverse=True
        )[:5]

        subject_performance = {}
        for attempt in monthly_attempts:
            subject_name = attempt.quiz.chapter.subject.title
            if subject_name not in subject_performance:
                subject_performance[subject_name] = {
                    "total_attempts": 0,
                    "total_score": 0,
                    "quizzes": [],
                }
            subject_performance[subject_name]["total_attempts"] += 1
            subject_performance[subject_name]["total_score"] += attempt.percentage_score
            subject_performance[subject_name]["quizzes"].append(attempt.quiz.title)

        for subject in subject_performance:
            subject_performance[subject]["average_score"] = (
                subject_performance[subject]["total_score"]
                / subject_performance[subject]["total_attempts"]
            )

    html_content = generate_html_report(
        user=user,
        month_year=f"{first_day.strftime('%B %Y')}",
        total_quizzes=total_quizzes,
        unique_quiz_count=unique_quiz_count,
        average_score=round(average_score, 1),
        highest_score=round(highest_score, 1),
        lowest_score=round(lowest_score, 1),
        ranking_position=ranking_position,
        recent_attempts=recent_attempts,
        subject_performance=subject_performance,
    )

    msg = Message(
        subject=f"Monthly Activity Report - {first_day.strftime('%B %Y')}",
        recipients=[user.email],
        html=html_content,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )

    mail.send(msg)


def generate_html_report(
    user,
    month_year,
    total_quizzes,
    unique_quiz_count,
    average_score,
    highest_score,
    lowest_score,
    ranking_position,
    recent_attempts,
    subject_performance,
):
    """Generate HTML content for the monthly report"""

    # Generate subject performance HTML
    subject_html = ""
    if subject_performance:
        subject_html = "<h3>📚 Subject-wise Performance</h3>"
        for subject, data in subject_performance.items():
            subject_html += f"""
            <div class="subject-card">
                <div class="subject-header">
                    <strong>{subject}</strong>
                    <span class="subject-score">{round(data['average_score'], 1)}%</span>
                </div>
                <div class="subject-details">
                    {data['total_attempts']} quiz{'s' if data['total_attempts'] > 1 else ''} taken
                </div>
            </div>
            """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
            .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; margin: 20px 0; }}
            .stat-card {{ background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; margin-bottom: 5px; }}
            .stat-label {{ font-size: 0.9em; color: #666; }}
            .recent-quizzes {{ margin-top: 25px; }}
            .quiz-item {{ background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; border-radius: 5px; }}
            .performance-badge {{ display: inline-block; padding: 8px 16px; border-radius: 20px; font-weight: bold; margin: 10px 0; }}
            .top-performer {{ background: #d4edda; color: #155724; }}
            .above-average {{ background: #d1ecf1; color: #0c5460; }}
            .below-average {{ background: #f8d7da; color: #721c24; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 0.9em; }}
            .subject-card {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .subject-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }}
            .subject-score {{ font-weight: bold; color: #667eea; }}
            .subject-details {{ font-size: 0.9em; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Monthly Activity Report</h1>
            <h2>{month_year}</h2>
            <p>Hello {user.username}!</p>
        </div>
        
        <div class="content">
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-number">{total_quizzes}</div>
                    <div class="stat-label">Quizzes Taken</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{unique_quiz_count}</div>
                    <div class="stat-label">Unique Quizzes</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{average_score}%</div>
                    <div class="stat-label">Average Score</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{highest_score}%</div>
                    <div class="stat-label">Highest Score</div>
                </div>
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <span class="performance-badge {'top-performer' if 'Top' in ranking_position else 'above-average' if 'Above' in ranking_position else 'below-average'}">
                    🏆 {ranking_position} Performance
                </span>
            </div>
            
            {subject_html}
            
            <div class="recent-quizzes">
                <h3>📝 Recent Quiz Activity</h3>
                {generate_recent_quizzes_html(recent_attempts)}
            </div>
            
            <div class="footer">
                <p>Keep up the great work! 🎯</p>
                <p><small>This report was generated automatically on {datetime.now().strftime('%B %d, %Y')}</small></p>
            </div>
        </div>
    </body>
    </html>
    """

    return html_content


def generate_recent_quizzes_html(recent_attempts):
    """Generate HTML for recent quiz attempts"""
    if not recent_attempts:
        return "<p>No recent quiz activity found.</p>"

    html = ""
    for attempt in recent_attempts:
        score_color = (
            "#28a745"
            if attempt.percentage_score >= 80
            else "#ffc107" if attempt.percentage_score >= 60 else "#dc3545"
        )
        html += f"""
        <div class="quiz-item">
            <strong>{attempt.quiz.title}</strong>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                <span style="color: {score_color}; font-weight: bold;">{round(attempt.percentage_score, 1)}%</span>
                <span style="color: #666; font-size: 0.9em;">{attempt.submit_datetime.strftime('%B %d, %Y')}</span>
            </div>
        </div>
        """
    return html


def send_no_activity_report(user, month, year):
    """Send a different report when user has no activity"""
    month_name = datetime(year, month, 1).strftime("%B")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Monthly Activity Report</h1>
            <h2>{month_name} {year}</h2>
            <p>Hello {user.username}!</p>
        </div>
        
        <div class="content">
            <h3>📝 No Quiz Activity This Month</h3>
            <p>We noticed you didn't take any quizzes in {month_name}. That's okay!</p>
            <p>Ready to jump back in? We have lots of exciting quizzes waiting for you!</p>
            <p style="margin-top: 30px;">
                <a href="#" style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px;">
                    Take a Quiz Now
                </a>
            </p>
        </div>
    </body>
    </html>
    """

    msg = Message(
        subject=f"Monthly Activity Report - {month_name} {year}",
        recipients=[user.email],
        html=html_content,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )

    mail.send(msg)


def generate_quiz_stats_csv(user_id, output_path=None):
    if output_path is None:
        output_path = os.path.join(
            current_app.config.get("UPLOAD_FOLDER", "static/exports"),
            f'quiz_stats_{user_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    stats_data = []
    with orm.db_session:
        user = User.get(id=user_id, is_deleted=False)

        attempts = orm.select(
            qa for qa in QuizAttempt if qa.user.id == user_id and not qa.is_deleted
        )

        for attempt in attempts:
            quiz = attempt.quiz
            chapter = quiz.chapter
            subject = chapter.subject
            remarks = (
                "Pass"
                if attempt.percentage_score >= quiz.passing_percentage
                else "Fail"
            )

            stats_data.append(
                {
                    "quiz_id": quiz.id,
                    "chapter_id": chapter.id,
                    "quiz_title": quiz.title,
                    "chapter_title": chapter.title,
                    "subject_title": subject.title,
                    "date_of_quiz": attempt.submit_datetime.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "score": attempt.score,
                    "total_marks": quiz.total_marks,
                    "percentage_score": round(attempt.percentage_score, 2),
                    "remarks": remarks,
                }
            )

    headers = [
        "quiz_id",
        "chapter_id",
        "quiz_title",
        "chapter_title",
        "subject_title",
        "date_of_quiz",
        "score",
        "total_marks",
        "percentage_score",
        "remarks",
    ]
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in stats_data:
            writer.writerow(row)

    send_quiz_stats_email(output_path, user_email, stats_data)


def send_quiz_stats_email(csv_path, user_email, stats_data):
    """
    Send an email to the user with quiz statistics summary in HTML and CSV attachment.
    """
    subject = "📊 Your Quiz Statistics Export is Ready!"

    html_content = render_template_string(
        """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            h2 { color: #2e6c80; }
            .summary { background-color: #f9f9f9; padding: 10px; border-radius: 5px; }
            p { line-height: 1.6; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Quiz Statistics Export</h2>
            <p>Dear User,</p>
            <p>Your quiz statistics export is ready! We've attached a detailed CSV file for your reference.</p>
            <div class="summary">
                <p><strong>Total Quizzes Attempted:</strong> {{ total_quizzes }}</p>
                <p><strong>Average Percentage Score:</strong> {{ avg_score }}%</p>
            </div>
            <p>Thank you for using our platform!</p>
            <p>Best regards,<br><em>Quiz App Team</em></p>
        </div>
    </body>
    </html>
    """,
        total_quizzes=len(stats_data),
        avg_score=round(
            (
                sum(d["percentage_score"] for d in stats_data) / len(stats_data)
                if stats_data
                else 0
            ),
            2,
        ),
    )

    msg = Message(subject=subject, recipients=[user_email], html=html_content)

    # Attach the CSV file
    with open(csv_path, "rb") as f:
        msg.attach(
            filename=os.path.basename(csv_path), content_type="text/csv", data=f.read()
        )

    mail.send(msg)
    return f"Email sent to {user_email} with attachment {csv_path}"
