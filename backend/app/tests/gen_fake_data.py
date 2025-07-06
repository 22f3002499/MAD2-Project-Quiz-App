from datetime import datetime, timedelta
import random
from faker import Faker
from pony import orm
import os

from app.models.database import (
    User,
    Subject,
    Quiz,
    Question,
    Option,
    QuizAttempt,
    Chapter,
    UserAnswer,
    init_db,
)

fake = Faker()


@orm.db_session
def create_fake_users(count=10):
    """Create fake users with valid data"""
    print(f"Creating {count} fake users...")
    users = []
    for _ in range(count):
        # Generate birthday for users between 18 and 60 years old
        dob = fake.date_of_birth(minimum_age=18, maximum_age=60)

        # Create user with unique email and username
        try:
            user = User(
                email=fake.unique.email(),
                username=fake.unique.user_name(),
                password="password123",  # Will be hashed by before_insert
                date_of_birth=dob,
                is_admin=fake.boolean(
                    chance_of_getting_true=10
                ),  # 10% chance of being admin
                last_login=fake.date_time_between(start_date="-30d", end_date="now"),
                is_deleted=fake.boolean(
                    chance_of_getting_true=5
                ),  # 5% chance of being deleted
                is_banned=fake.boolean(
                    chance_of_getting_true=3
                ),  # 3% chance of being banned
            )
            users.append(user)
        except Exception as e:
            print(f"Error creating user: {e}")

    return users


@orm.db_session
def create_fake_subjects(count=5):
    """Create fake subjects linked to random users"""
    print(f"Creating {count} fake subjects...")
    subjects = []

    # Get all active users
    users = list(User.select(lambda u: not u.is_deleted and not u.is_banned))
    if not users:
        print("No active users found. Creating subjects failed.")
        return subjects

    for _ in range(count):
        try:
            subject = Subject(
                title=fake.catch_phrase(),
                description=fake.paragraph(),
                user=random.choice(users),
                is_deleted=fake.boolean(
                    chance_of_getting_true=5
                ),  # 5% chance of being deleted
            )
            subjects.append(subject)
        except Exception as e:
            print(f"Error creating subject: {e}")

    return subjects


@orm.db_session
def create_fake_chapters(count=5):
    """Create fake subjects linked to random users"""
    print(f"Creating {count} fake subjects...")
    chapters = []
    subjects = orm.select(sub for sub in Subject)[:]

    for sub in subjects:
        for _ in range(count):
            try:
                chapter = Chapter(
                    title=fake.catch_phrase(),
                    description=fake.paragraph(),
                    subject=random.choice(subjects),
                    is_deleted=fake.boolean(
                        chance_of_getting_true=5
                    ),  # 5% chance of being deleted
                )
                chapters.append(chapter)
            except Exception as e:
                print(f"Error creating subject: {e}")

    return chapters


@orm.db_session
def create_fake_quizzes(count=30):
    """Create fake quizzes linked to random subjects"""
    print(f"Creating {count} fake quizzes...")
    quizzes = []

    # Get all active subjects
    chapters = list(Chapter.select(lambda s: not s.is_deleted))
    if not chapters:
        print("No active subjects found. Creating quizzes failed.")
        return quizzes

    for _ in range(count):
        # Create quiz with valid duration and start time
        try:
            duration = random.randint(10, 120)  # 10 to 120 minutes
            attempts_allowed = random.randint(1, 5)  # 1 to 5 attempts allowed

            # Start time must be in the future relative to creation time
            start_time = datetime.now() + timedelta(days=random.randint(1, 30))

            quiz = Quiz(
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(),
                duration=duration,
                start_datetime=start_time,
                created_at=start_time - timedelta(days=2),
                chapter=random.choice(chapters),
                is_deleted=fake.boolean(
                    chance_of_getting_true=5
                ),  # 5% chance of being deleted
                attempts_allowed=attempts_allowed,
            )
            quizzes.append(quiz)
        except Exception as e:
            print(f"Error creating quiz: {e}")

    return quizzes


@orm.db_session
def create_fake_questions(count_per_quiz=5):
    """Create fake questions for each quiz respecting the total_questions limit"""
    print("Creating fake questions for quizzes...")
    questions_created = 0

    # Get all active quizzes
    quizzes = list(Quiz.select(lambda q: not q.is_deleted))
    if not quizzes:
        print("No active quizzes found. Creating questions failed.")
        return 0

    for quiz in quizzes:
        # Determine how many questions to create for this quiz
        num_questions = random.randint(3, count_per_quiz)

        for _ in range(num_questions):
            try:

                # Determine if MCQ or MSQ
                is_msq = fake.boolean(chance_of_getting_true=30)  # 30% chance of MSQ

                question = Question(
                    title=fake.sentence(nb_words=6) + "?",
                    description=(
                        fake.paragraph()
                        if fake.boolean(chance_of_getting_true=70)
                        else ""
                    ),
                    quiz=quiz,
                    marks=random.randint(1, 10),
                    is_deleted=fake.boolean(
                        chance_of_getting_true=5
                    ),  # 5% chance of being deleted
                    _type=is_msq,  # False=MCQ, True=MSQ
                    # No image for simplicity
                )

                # Create options for this question
                create_fake_options(question, random.randint(3, 6))
                questions_created += 1
            except Exception as e:
                print(f"Error creating question: {e}")

    return questions_created


@orm.db_session
def create_fake_options(question, count=4):
    """Create fake options for a question with at least one correct answer"""
    options = []

    # Ensure at least one correct answer
    correct_option_index = random.randint(0, count - 1)

    for i in range(count):
        is_correct = False

        # For MCQ, only one option is correct
        if question.type == "MCQ":  # MCQ
            is_correct = i == correct_option_index
        else:  # MSQ
            # For MSQ, randomly decide if an option is correct with a bias towards having multiple correct answers
            if i == correct_option_index:
                is_correct = True
            else:
                is_correct = fake.boolean(chance_of_getting_true=40)  # 40% chance

        try:
            option = Option(
                title=fake.sentence(nb_words=3),
                description=(
                    fake.sentence() if fake.boolean(chance_of_getting_true=30) else ""
                ),
                question=question,
                is_deleted=fake.boolean(
                    chance_of_getting_true=5
                ),  # 5% chance of being deleted
                is_correct=is_correct,
                # No image for simplicity
            )
            question.options.add(option)
            options.append(option)
        except Exception as e:
            print(f"Error creating option: {e}")

    return options


@orm.db_session
def create_fake_quiz_attempts():
    """Create fake quiz attempts for users"""
    print("Creating fake quiz attempts...")
    attempts_created = 0

    # Get active users
    users = list(User.select(lambda u: not u.is_deleted and not u.is_banned))
    if not users:
        print("No active users found. Creating attempts failed.")
        return 0

    # Get quizzes that have started
    current_time = datetime.now()
    past_quizzes = list(Quiz.select(lambda q: not q.is_deleted))

    for quiz in past_quizzes:
        eligible_users = random.sample(
            users, min(len(users), 5)
        )  # Up to 5 random users per quiz

        for user in eligible_users:
            # Check if user hasn't exceeded attempts limit
            attempt_count = orm.count(
                qa
                for qa in QuizAttempt
                if qa.quiz == quiz and qa.user == user and not qa.is_deleted
            )

            if attempt_count < quiz.attempts_allowed:
                try:
                    submit_time = fake.date_time_between(
                        start_date=quiz.start_datetime, end_date=current_time
                    )

                    quiz_attempt = QuizAttempt(
                        quiz=quiz,
                        user=user,
                        score=0,  # Will be calculated after answers are created
                        percentage_score=0,  # Will be calculated after score
                        submit_datetime=submit_time,
                        is_deleted=fake.boolean(
                            chance_of_getting_true=5
                        ),  # 5% chance of being deleted
                    )

                    # Create user answers for this attempt
                    create_user_answers(quiz_attempt)

                    # Calculate scores
                    quiz_attempt.calc_score()
                    quiz_attempt.calc_percentage_score()

                    attempts_created += 1
                except Exception as e:
                    print(f"Error creating quiz attempt: {e}")

    return attempts_created


@orm.db_session
def create_user_answers(quiz_attempt):
    """Create fake user answers for a quiz attempt"""
    answers_created = 0

    # Get questions for the quiz
    questions = list(
        Question.select(lambda q: q.quiz == quiz_attempt.quiz and not q.is_deleted)
    )

    for question in questions:
        # Sometimes skip questions to simulate incomplete quiz

        try:
            # Get valid options for this question
            available_options = list(
                Option.select(lambda o: o.question == question and not o.is_deleted)
            )

            if not available_options:
                continue

            user_answer = UserAnswer(quiz_attempt=quiz_attempt, question=question)

            # Handle MCQ vs MSQ answers
            if not question.type:  # MCQ
                # Select one random option
                selected_option = random.choice(available_options)
                user_answer.options.add(selected_option)
            else:  # MSQ
                # Select random number of options (at least 1)
                num_options = random.randint(1, len(available_options))
                selected_options = random.sample(available_options, num_options)
                for option in selected_options:
                    user_answer.options.add(option)

            answers_created += 1
        except Exception as e:
            print(f"Error creating user answer: {e}")

    return answers_created


@orm.db_session
def print_statistics():
    """Print statistics about the generated data"""
    print("\n--- DATABASE STATISTICS ---")
    print(f"Users: {orm.count(u for u in User)}")
    print(f"Subjects: {orm.count(s for s in Subject)}")
    print(f"Quizzes: {orm.count(q for q in Quiz)}")
    print(f"Questions: {orm.count(q for q in Question)}")
    print(f"Options: {orm.count(o for o in Option)}")
    print(f"Quiz Attempts: {orm.count(qa for qa in QuizAttempt)}")
    print(f"User Answers: {orm.count(ua for ua in UserAnswer)}")
    print("-------------------------")


def generate_fake_data():
    """Main function to generate all fake data"""

    # Remove database if exists
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    db_path = os.path.join(base_dir, os.environ.get("DATABASE") or "quiz_app.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    # Initialize database
    init_db()

    with orm.db_session:
        # Create fake data
        users = create_fake_users(15)
        subjects = create_fake_subjects(30)
        chapters = create_fake_chapters()

        orm.flush()
        orm.commit()
        quizzes = create_fake_quizzes(50)

        # Commit transaction to ensure IDs are generated
        orm.commit()

        question_count = create_fake_questions()

        # # Commit transaction again
        orm.commit()

        attempt_count = create_fake_quiz_attempts()
        orm.commit()

        # Print statistics
        # print_statistics()

        # print(f"\nSuccessfully created:")
        # print(f"- {len(users)} users")
        # print(f"- {len(subjects)} subjects")
        # print(f"- {len(quizzes)} quizzes")
        # print(f"- {question_count} questions")
        # print(f"- {attempt_count} quiz attempts")

        # print("\nFake data generation complete!")
