from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_app_settings

# SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"

SETTINGS = get_app_settings()

engine = create_engine(
    SETTINGS.database_url,
    # required for sqlite
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
