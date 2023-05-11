from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from app.core.auth import oauth2_scheme
from app.db.session import SETTINGS, SessionLocal
from app.models.user import User


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:  # type: ignore [type-arg]
    db = SessionLocal()
    db.current_user_id = None  # type: ignore [attr-defined]
    try:  # noqa: WPS501 Found `finally` in `try` block without `except`
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            SETTINGS.secret_key,
            algorithms=[SETTINGS.algorithm],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
