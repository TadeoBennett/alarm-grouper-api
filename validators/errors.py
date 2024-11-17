from werkzeug.exceptions import HTTPException
from flask_smorest import abort

class NotFoundError(HTTPException):
    def __init__(self, message):
        if message != "" and message is not None:
            self.message = f"Resource not found: {message}"
        else:
            self.message = "Resource not found"
        self.code = 404
        self.description = "The requested resource was not found!"
        self.error_response={"Error": self.message, "code": self.code, "message": self.description}
        print(self.message)


class ServerError(HTTPException):
    def __init__(self, message):
        if message == ""  or message is None:
            message = "Internal Server Error"
        else:
            message = f"Internal Server Error: {message}"
        self.code = 500
        self.description = "Something went wrong!"
        self.message = message
        self.error_response={"Error": self.message, "code": self.code, "message": self.description}
        print(self.message)


class CustomValidationError(HTTPException):
    def __init__(self, message):
        self.message = f"{message}"
        self.code = 400
        self.description = "Request payload is invalid!"
        self.error_response={"Error": self.message, "code": self.code, "message": self.description}
        print(self.message)

class EmailExistsError(HTTPException):
    def __init__(self, email):
        self.message = f"Bad Request, Email Exists Error"
        self.code = 400
        self.description = f"Email '{email}' already exists!"
        self.error_response={"Error": self.message, "code": self.code, "message": self.description}
        print(self.message)

class ForbiddenError(HTTPException):
    def __init__(self):
        self.message = f"Bad Request, Not Allowed Error"
        self.code = 403
        self.description = "Request is Forbidden!"
        self.error_response={"Error": self.message, "code": self.code, "message": self.description}
        print(self.message)
        

class DuplicateError(HTTPException):
    def __init__(self, resource):
        self.message = f"Bad Request, Duplicate Error"
        self.code = 400
        self.description = f"Resource '{resource}' already exists!"
        self.error_response={"Error": self.message, "code": self.code, "message": self.description}
        print(self.message)