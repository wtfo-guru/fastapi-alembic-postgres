from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base

KMAX256 = 256
KMAX39 = 39

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

class Banned(Base):
    """Model class for banned table."""
    id = Column(Integer, primary_key=True, index=True)
    addr = Column(String(KMAX39), index=True, nullable=False)
    jail_id = relationship(
        "Recipe",
        cascade="all,delete-orphan",
        back_populates="submitter",
        uselist=True,
    )

    jail_id = mapped_column(ForeignKey("jail.id"))
    bans: Mapped[Jail] = relationship(back_populates="ipaddrs")

    def __repr__(self) -> str:
        return "Address(id={0}, ip_address={1}, jail_id={2})".format(
            self.id,
            self.addr,
            self.jail_id,
        )
