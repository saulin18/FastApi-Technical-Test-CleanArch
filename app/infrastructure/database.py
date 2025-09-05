
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings


engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=300,
)

def get_db() -> Session: # type: ignore
   
    with get_session() as session:
        yield session
        
def get_session() -> Session:
    return Session(engine)
        
def create_tables():

    SQLModel.metadata.create_all(engine)
