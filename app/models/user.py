from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

KMAX256 = 256

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(KMAX256), nullable=True)
    password = Column(String(KMAX256), nullable=True)
    email = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
    authenticated = Column(Boolean, default=False)
    recipes = relationship(
        "Recipe",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )
