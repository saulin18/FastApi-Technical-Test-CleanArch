class ApplicationException(Exception):
    
    pass


class ServiceException(ApplicationException):
   
    def __init__(self, message: str):
        super().__init__(message)


class TaskNotFound(ApplicationException):
    
    def __init__(self):
        super().__init__("Task not found")


class UserNotFound(ApplicationException):
  
    def __init__(self):
        super().__init__("User not found")


class AuthenticationFailed(ApplicationException):
   
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class InvalidCredentials(ApplicationException):
    
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)
