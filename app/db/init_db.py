import logging
from typing import Optional, Tuple

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.hashing import Hasher

logger = logging.getLogger(__name__)

INVALID_FIRST_SUPERUSER = """Skipping creating superuser. fsu needs to be
provided as an env variable. e.g. fsu=username:password"""

EXISTING_FIRST_SUPERUSER: str = (
    "Skipping creating superuser. User with username {0} already exists."
)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def parse_first_superuser(fsu: str) -> Tuple[str, ...]:
    """Parse the first superuser."""
    parts = fsu.split(":")
    nbr_parts = len(parts)
    if nbr_parts < 2:
        raise ValueError(INVALID_FIRST_SUPERUSER)
    if not parts[0]:
        raise ValueError(INVALID_FIRST_SUPERUSER)
    if not parts[1]:
        raise ValueError(INVALID_FIRST_SUPERUSER)
    if nbr_parts > 2:
        return (parts[0], parts[1], parts[2])
    return (parts[0], parts[1], "")


def init_db(db: Session, fsu: str) -> None:  # noqa: WPS210
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    try:
        if fsu:
            username, password, addr = parse_first_superuser(fsu)
            email: Optional[EmailStr] = None
            if addr:
                email = EmailStr(addr)
            user = crud.user.get_by_name(db, name=username)
            if user:
                raise ValueError(EXISTING_FIRST_SUPERUSER.format(username))
            else:
                user_in = schemas.UserCreate(
                    username=username,
                    password=Hasher.get_password_hash(password),
                    email=email,
                    is_superuser=True,
                )
                user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            raise ValueError(INVALID_FIRST_SUPERUSER)
    except ValueError as ex:
        logger.warning(str(ex))
