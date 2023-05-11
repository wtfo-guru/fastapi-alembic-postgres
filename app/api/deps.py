from typing import Generator

from app.db.session import SessionLocal


def get_db() -> Generator:  # type: ignore [type-arg]
    db = SessionLocal()
    db.current_user_id = None  # type: ignore [attr-defined]
    try:  # noqa: WPS501 Found `finally` in `try` block without `except`
        yield db
    finally:
        db.close()
