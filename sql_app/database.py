from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./todo_app.db"  # SQLite database URL
# DATABASE_URL = "postgresql://user:password@postgresserver/db" # PostgreSQL database URL

engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
