
from uuid import UUID
from datetime import datetime



class User:
    def __init__(self, id: UUID, name: str, email: str, password: str, created_at: datetime, updated_at: datetime):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
    
    
    