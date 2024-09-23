from werkzeug.exceptions import HTTPException
from flask_smorest import abort

class NotFoundError(HTTPException):
    def __init__(self, resource):
        self.message = f"{resource} not found"
        self.code = 404
        self.description = "The requested resource was not found!"


class ServerError(HTTPException):
    def __init__(self):
        self.message = f"Internal Server Error"
        self.code = 500
        self.description = "Something went wrong!"


class CustomValidationError(HTTPException):
    def __init__(self):
        self.message = f"Bad Request, Validation Error"
        self.code = 400
        self.description = "Request payload is invalid!"

class EmailExistsError(HTTPException):
    def __init__(self, email):
        self.message = f"Bad Request, Email Exists Error"
        self.code = 400
        self.description = f"Email '{email}' already exists!"

class ForbiddenError(HTTPException):
    def __init__(self):
        self.message = f"Bad Request, Not Allowed Error"
        self.code = 403
        self.description = "Request is Forbidden!"