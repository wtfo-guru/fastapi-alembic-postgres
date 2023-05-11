from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.hashing import Hasher
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[User]:
        return db.query(User).filter(User.username == name).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        create_data = obj_in.dict()
        create_data["password"] = Hasher.get_password_hash(obj_in.password)
        db_obj = User(**create_data)
        db.add(db_obj)
        db.commit()
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]],  # noqa: WPS221
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data["passwords"] = Hasher.get_password_hash(update_data["passwords"])
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        return False if user.is_superuser is None else user.is_superuser


user = CRUDUser(User)
