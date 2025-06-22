class APIException(Exception):
    message = "An error occured"
    status_code = 500
    """
        message: response error message
        payload: additional data to include in response
    """

    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__(message or __class__.message)
        self.message = message if message is not None else type(self).message
        self.status_code = (
            status_code if status_code is not None else type(self).status_code
        )
        self.payload = payload

    def to_dict(self):
        """
        converts to exception to dictionary for JSON serilization
        """
        error_dict = dict(self.payload or {})
        error_dict["error"] = self.message
        return error_dict


class ResourceNotFoundException(APIException):
    status_code = 404
    message = "Resource not found"


class AuthenticationException(APIException):
    status_code = 401
    message = "Authentication failed"


class JWTTokenException(APIException):
    status_code = 400
    message = "Invalid jwt token"


class QuizException(APIException):
    status_code = 400
    message = "something went wrong while fetching quizzes"


class QuizAttemptException(APIException):
    status_code = 400
    message = "something went wrong while fetching quiz_attempt"


class ResourceException(APIException):
    status_code = 400
    message = "invalid resource"
