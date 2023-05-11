from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(
    *,
    user_in: UserCreate,
    db: Session = Depends(deps.get_db),
) -> UserModel:
    """
    Create a new user in the database.
    """
    return crud.user.create(db=db, obj_in=user_in)
