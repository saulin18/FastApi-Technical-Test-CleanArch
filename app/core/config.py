
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    
    
    app_name: str = "FastAPI Clean Architecture TodoList"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database settings
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/todolist")
    
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

settings = Settings()
