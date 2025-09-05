class InfrastructureException(Exception):
   
    pass
     
class UserNotFound(InfrastructureException):

    def __init__(self):
        super().__init__("User not found")


class TaskNotFound(InfrastructureException):
    
    def __init__(self):
        super().__init__("Task not found")


class UserAlreadyExists(InfrastructureException):
   
    def __init__(self):
        super().__init__("User already exists")


class InvalidToken(InfrastructureException):
  
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)


class InvalidCredentials(InfrastructureException):
    
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)
