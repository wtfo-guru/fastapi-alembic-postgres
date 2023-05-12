from datetime import datetime, timedelta
from typing import List, MutableMapping, Optional, Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm.session import Session

from app.core.hashing import Hasher
from app.db.session import SETTINGS
from app.models.user import User

JWTPayloadMapping = MutableMapping[
    str,
    Union[datetime, bool, str, List[str], List[int]],
]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="{0}/auth/login".format(SETTINGS.api_prefix),
)


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not Hasher.verify_password(password, str(user.password)):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(  # noqa: S106
        token_type="access_token",
        lifetime=timedelta(minutes=SETTINGS.access_token_expire_minutes),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = str(expire)

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = str(datetime.utcnow())

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    return jwt.encode(payload, str(SETTINGS.secret_key), algorithm=SETTINGS.algorithm)
