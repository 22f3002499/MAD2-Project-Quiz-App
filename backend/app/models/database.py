from datetime import datetime, date
from pony import orm
import os
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash
from base64 import b64encode
from datetime import datetime

ENV_FILE = find_dotenv(r".env")
load_dotenv(ENV_FILE)

db = orm.Database()


# DEFINING TABLES
# self REFERS TO THE CURRENT INSTANCE/
# CURRENT ROW BEING INSERTED INTO THE ENTITIES/TABLES
class User(db.Entity):
    _table_ = "user"
    id = orm.PrimaryKey(int, auto=True)
    email = orm.Required(str, unique=True)
    username = orm.Required(str, unique=True)
    password = orm.Required(str)
    date_of_birth = orm.Optional(date)
    is_admin = orm.Required(bool, default=False)
    last_login = orm.Optional(datetime, default=datetime.now())
    is_deleted = orm.Required(bool, default=False)
    is_banned = orm.Required(bool, default=False)
    created_at = orm.Required(datetime, default=lambda: datetime.now())

    subjects = orm.Set("Subject")
    quiz_attempts = orm.Set("QuizAttempt")

    def before_insert(self):
        self.password = generate_password_hash(self.password)

    def soft_delete(self):
        self.is_deleted = True


class Subject(db.Entity):
    _table_ = "subject"
    id = orm.PrimaryKey(int, auto=True)
    title = orm.Required(str)
    description = orm.Optional(str, default="")
    is_deleted = orm.Required(bool, default=False)
    user = orm.Set(User)
    created_at = orm.Required(datetime, default=lambda: datetime.now())

    chapters = orm.Set("Chapter")

    def soft_delete(self):
        self.is_deleted = True
        for chapter in self.chapters:
            chapter.soft_delete()


class Chapter(db.Entity):
    _table_ = "chapter"
    id = orm.PrimaryKey(int, auto=True)
    title = orm.Required(str)
    description = orm.Optional(str, default="")
    is_deleted = orm.Required(bool, default=False)
    created_at = orm.Required(datetime, default=lambda: datetime.now())

    subject = orm.Required(Subject)
    quizzes = orm.Set("Quiz")

    def soft_delete(self):
        self.is_deleted = True
        for quiz in self.quizzes:
            quiz.soft_delete()


class Quiz(db.Entity):
    _table_ = "quiz"
    id = orm.PrimaryKey(int, auto=True)
    title = orm.Required(str)
    description = orm.Optional(str, default="")
    duration = orm.Required(int)  # Duration in minutes
    start_datetime = orm.Required(datetime)
    created_at = orm.Required(datetime, default=lambda: datetime.now())
    is_deleted = orm.Required(bool, default=False)
    # total_questions = orm.Required(int, default=1)
    # total_marks = orm.Required(int, default=0)
    attempts_allowed = orm.Required(int, default=1)
    passing_percentage = orm.Optional(float, default=33.0)

    questions = orm.Set("Question")
    quiz_attempts = orm.Set("QuizAttempt")
    chapter = orm.Required(Chapter)

    @property
    def total_questions(self):
        return orm.count(q for q in self.questions if not q.is_deleted)

    @property
    def total_marks(self):
        return orm.sum(q.marks for q in self.questions if not q.is_deleted)

    def before_insert(self):
        if self.duration <= 0:
            raise ValueError("Duration must be greater than 0")
        if self.start_datetime <= self.created_at:
            raise ValueError("Start datetime must be after creation time")

    # verify quiz total_questions limit
    def before_update(self):
        # question_count = orm.count(
        #     ques for ques in Question if ques.quiz == self and not ques.is_deleted
        # )
        # if question_count > self.total_questions:
        #     raise ValueError(
        #         f"Cannot decrease the limit of total_questions. Quiz has currently {question_count} active questions."
        #     )
        if self.start_datetime < datetime.now():
            raise ValueError(f"The quiz cannot be updated after it has started.")

    def soft_delete(self):
        self.is_deleted = True
        for qa in self.quiz_attempts:
            qa.soft_delete()


class Question(db.Entity):
    _table_ = "question"
    id = orm.PrimaryKey(int, auto=True)
    title = orm.Required(str)
    description = orm.Optional(str, default="")
    _image = orm.Optional(bytes)
    marks = orm.Required(int, default=0)
    is_deleted = orm.Required(bool, default=False)
    _type = orm.Required(bool, default=False)  # False=MCQ, True=MSQ
    created_at = orm.Required(datetime, default=lambda: datetime.now())

    quiz = orm.Required(Quiz)
    options = orm.Set("Option")
    user_answers = orm.Set("UserAnswer")

    # True = MSQ , False = MCQ
    @property
    def type(self) -> str:
        if self._type:
            return "MSQ"
        return "MCQ"

    def soft_delete(self):
        self.is_deleted = True
        for opt in self.options:
            opt.is_deleted = True

    @property
    def image(self):
        if self._image:
            return b64encode(self._image).decode("utf-8")
        return None

    def before_insert(self):
        if self.marks < 0:
            raise ValueError("Marks must be greater than or equal to 0")

        # verify quiz total_questions limit
        # question_count = orm.count(
        #     ques for ques in Question if ques.quiz == self.quiz and not ques.is_deleted
        # )
        # if question_count >= self.quiz.total_questions:
        #     raise ValueError(
        #         "Cannot add more questions than the quiz total_questions limit"
        #     )

    # def after_insert(self):
    #     # Update quiz total marks

    #     total_marks = orm.sum(
    #         ques.marks
    #         for ques in Question
    #         if ques.quiz == self.quiz and not ques.is_deleted
    #     )
    #     self.quiz.total_marks = total_marks

    # def before_update(self):
    #     # verify quiz total_questions limit when changing quiz
    #     old_question_quiz = self._dbvals_.get(Question.quiz)
    #     new_question_quiz = self.quiz

    #     if old_question_quiz != new_question_quiz:

    #         question_count = orm.count(
    #             ques
    #             for ques in Question
    #             if ques.quiz == self.quiz and not ques.is_deleted
    #         )
    # if question_count >= self.quiz.total_questions:
    #     raise ValueError(
    #         "Cannot add more questions than the quiz total_questions limit"
    #     )

    # # update total_marks of new quiz
    # self.quiz.total_marks = orm.sum(
    #     ques.marks
    #     for ques in Question
    #     if ques.quiz == self.quiz and not ques.is_deleted
    # )

    # # update total_marks of old quiz
    # old_question_quiz.total_marks = orm.sum(
    #     ques.marks
    #     for ques in Question
    #     if ques.quiz == self.quiz and not ques.is_deleted
    # )


class Option(db.Entity):
    _table_ = "option"
    id = orm.PrimaryKey(int, auto=True)
    title = orm.Required(str)
    description = orm.Optional(str, default="")
    _image = orm.Optional(bytes)
    is_deleted = orm.Required(bool, default=False)
    is_correct = orm.Required(bool, default=False)
    created_at = orm.Required(datetime, default=lambda: datetime.now())

    user_answers = orm.Set("UserAnswer")
    question = orm.Required(Question)

    @property
    def image(self):
        if self._image:
            return b64encode(self._image).decode("utf-8")
        return None

    def soft_delete(self):
        self.is_deleted = True

    def after_insert(self):
        self.update_question_type()
        print("inside after_insert")

    def after_update(self):
        self.update_question_type()
        print("inside after_update")

    def update_question_type(self):
        ques = self.question
        correct_count = orm.sum(
            opt.is_correct for opt in ques.options if not opt.is_deleted
        )
        print(correct_count)

        if correct_count > 1:
            ques._type = True
        else:
            ques._type = False


class QuizAttempt(db.Entity):
    _table_ = "quiz_attempt"
    id = orm.PrimaryKey(int, auto=True)
    quiz = orm.Required(Quiz)
    user = orm.Required(User)
    score = orm.Required(float, default=0)
    percentage_score = orm.Required(float, default=0, max=float(100))
    submit_datetime = orm.Required(datetime, default=datetime.now())
    is_deleted = orm.Required(bool, default=False)
    created_at = orm.Required(datetime, default=lambda: datetime.now())

    user_answers = orm.Set("UserAnswer")

    def soft_delete(self):
        self.is_deleted = True

    def calc_score(self):
        if not self.user_answers:
            return

        score = 0
        for ua in self.user_answers:
            question = ua.question

            # MCQ TYPE QUESTION
            if question.type == False:
                score += question.marks if list(ua.options)[0].is_correct else 0

            # MSQ TYPE QUESTION
            elif question.type == True:
                all_selected_options_correct = all(opt.is_correct for opt in ua.options)
                if all_selected_options_correct:
                    total_options_answered = len(ua.options)
                    total_options_present = len(question.options)
                    score += (
                        total_options_answered / total_options_present
                    ) * question.marks

        self.score = score
        return

    def before_insert(self):

        if self.score < 0:
            raise ValueError("Score must be greater than or equal to 0")
        if self.percentage_score > 100:
            raise ValueError("Percentage score must be less than or equal to 100")

        # Check attempt limit (equivalent to check_attempt_allowed trigger)
        attempt_count = orm.count(
            qa
            for qa in QuizAttempt
            if qa.quiz == self.quiz and qa.user == self.user and not qa.is_deleted
        )
        if attempt_count >= self.quiz.attempts_allowed:
            raise ValueError(
                "Cannot add more attempts than the quiz attempt_allowed limit"
            )

    def calc_percentage_score(self):
        if self.quiz.total_marks > 0:
            self.percentage_score = (self.score / self.quiz.total_marks) * 100

    def before_update(self):
        if self.percentage_score > 100:
            raise ValueError("percent score cannot be more than 100")


class UserAnswer(db.Entity):
    _table_ = "user_answer"
    id = orm.PrimaryKey(int, auto=True)
    quiz_attempt = orm.Required(QuizAttempt)
    question = orm.Required(Question)
    options = orm.Set(Option)
    created_at = orm.Required(datetime, default=lambda: datetime.now())

    # Enforce unique combo of quiz_attempt, question, and option
    orm.composite_key(quiz_attempt, question)


def create_default_subjects():
    """Create default subjects with the admin user"""
    default_subjects_data = [
        {
            "title": "Mathematics",
            "description": "Covers algebra, geometry, calculus, and other mathematical concepts",
        },
        {
            "title": "Science",
            "description": "General science including physics, chemistry, and biology",
        },
        {
            "title": "English",
            "description": "English language, literature, grammar, and comprehension",
        },
        {
            "title": "History",
            "description": "World history, historical events, and important figures",
        },
        {
            "title": "Computer Science",
            "description": "Programming, algorithms, data structures, and computer fundamentals",
        },
        {
            "title": "General Knowledge",
            "description": "Current affairs, general awareness, and miscellaneous topics",
        },
    ]

    with orm.db_session:
        existing_subjects = orm.count(s for s in Subject if not s.is_deleted)

        if existing_subjects == 0:
            print("Creating default subjects...")
            for subject_data in default_subjects_data:
                subject = Subject(
                    title=subject_data["title"],
                    description=subject_data["description"],
                )

            orm.commit()


def init_db():
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    db_path = os.path.join(base_dir, os.environ.get("DATABASE") or "quiz_app.db")
    db.bind(provider="sqlite", filename=db_path, create_db=True)

    # Create tables
    db.generate_mapping(create_tables=True)

    create_default_subjects()
