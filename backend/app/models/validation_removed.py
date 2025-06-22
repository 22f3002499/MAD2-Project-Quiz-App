from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime


# Custom field for images
class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError("Invalid input type")

        if value is None or value == b"":
            raise ValidationError("Invalid value")


class SubjectSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String()
    is_deleted = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class ChapterSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    description = fields.String()
    subject_id = fields.Integer(required=True)
    is_deleted = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    password = fields.String(required=True, validate=validate.Length(min=8))
    date_of_birth = fields.Date(dump_default=None, load_default=None)
    is_admin = fields.Boolean(dump_only=True)
    last_login = fields.DateTime(dump_only=True)
    subject_id = fields.List(
        fields.Integer(validate=validate.Range(min=0)),
        required=True,
        validate=validate.Length(min=1),
    )


class LoginSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=50))
    password = fields.String(required=True, validate=validate.Length(min=8))


class QuizSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    description = fields.String()
    duration = fields.Integer(required=True, validate=validate.Range(min=1))
    start_datetime = fields.DateTime(required=True)
    created_at = fields.DateTime(dump_only=True)
    chapter_id = fields.Integer(required=True)
    total_questions = fields.Integer(required=True, validate=validate.Range(min=1))
    attempts_allowed = fields.Integer(required=True, validate=validate.Range(min=1))
    is_deleted = fields.Boolean(dump_only=True)

    @validates("start_datetime")
    def validate_start_datetime(self, start_datetime):
        if start_datetime <= datetime.now():
            raise ValidationError("Start datetime must be in the future")


class QuestionSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    image = BytesField()  # For binary data
    quiz_id = fields.Integer(required=True)
    marks = fields.Integer(validate=validate.Range(min=0))
    is_deleted = fields.Boolean(dump_only=True)
    type = fields.Boolean()  # 0 for MCQ, 1 for MSQ
    created_at = fields.DateTime(dump_only=True)


class OptionSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    image = BytesField()  # For binary data
    question_id = fields.Integer(required=True)
    is_deleted = fields.Boolean(dump_only=True)
    is_correct = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)


class QuizAttemptSchema(Schema):
    id = fields.Integer(dump_only=True)
    quiz_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    score = fields.Float(validate=validate.Range(min=0))
    submit_datetime = fields.DateTime(required=True)
    is_deleted = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


class EditQuiz(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(validate=validate.Length(min=1, max=200))
    description = fields.String()
    duration = fields.Integer(validate=validate.Range(min=1))
    start_datetime = fields.DateTime()
    chapter_id = fields.Integer()
    is_deleted = fields.Boolean(dump_only=True)
    total_questions = fields.Integer(validate=validate.Range(min=1))
    created_at = fields.DateTime(dump_only=True)

    @validates("start_datetime")
    def validate_start_datetime(self, start_datetime):
        if start_datetime <= datetime.now():
            raise ValidationError("Start datetime must be in the future")
