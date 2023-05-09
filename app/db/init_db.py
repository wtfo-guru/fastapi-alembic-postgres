import logging
from os import getenv
from typing import Optional, cast

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401

logger = logging.getLogger(__name__)

INVALID_FIRST_SUPERUSER = """Skipping creating superuser. FIRST_SUPERUSER needs to be
provided as an env variable. e.g. FIRST_SUPERUSER=username:password"""

FIRST_SUPERUSER = getenv("FIRST_SUPERUSER", "admin:secret")

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    try:
        if FIRST_SUPERUSER:
            parts = FIRST_SUPERUSER.split(":")
            nbr_parts = len(parts)
            if nbr_parts < 2:
                raise ValueError(INVALID_FIRST_SUPERUSER)
            if not parts[0]:
                raise ValueError(INVALID_FIRST_SUPERUSER)
            if not parts[1]:
                raise ValueError(INVALID_FIRST_SUPERUSER)
            email: Optional[EmailStr] = (
                cast(EmailStr, parts[2]) if nbr_parts > 2 else None
            )
            user = crud.user.get_by_name(db, name=parts[0])
            if not user:
                user_in = schemas.UserCreate(
                    username=parts[0],
                    password=parts[1],  # TODO: encrypted
                    email=email,
                    is_superuser=True,
                )
                user = crud.user.create(db, obj_in=user_in)  # noqa: F841
            else:
                raise ValueError(
                    "Skipping creating superuser. "
                    "User with username {0} already exists.".format(parts[0])
                )

        else:
            raise ValueError(INVALID_FIRST_SUPERUSER)
    except ValueError as ex:
        logger.warning(str(ex))
