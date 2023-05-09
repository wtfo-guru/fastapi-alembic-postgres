from sqlalchemy import Boolean, Column, Integer, String

from app.db.base_class import KCHARS256, Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(KCHARS256), nullable=False)
    password = Column(String(KCHARS256), nullable=False)
    email = Column(String, nullable=True)
    is_superuser = Column(Boolean, default=False)
    is_authenticated = Column(Boolean, default=False)
