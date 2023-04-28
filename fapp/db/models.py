from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for models."""


class Jail(Base):
    """Model class for jail table"""

    __tablename__ = "jail"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))  # noqa: WPS432
    ipaddrs: Mapped[List["Banned"]] = relationship(back_populates="bans")

    def __repr__(self) -> str:
        return "User(id={0}, name={1}".format(self.id, self.name)


class Banned(Base):
    """Model class for banned table."""

    __tablename__ = "banned"
    id: Mapped[int] = mapped_column(primary_key=True)
    addr: Mapped[str] = mapped_column(String(39))  # noqa: WPS432
    jail_id = mapped_column(ForeignKey("jail.id"))
    bans: Mapped[Jail] = relationship(back_populates="ipaddrs")

    def __repr__(self) -> str:
        return "Address(id={0}, ip_address={1}, jail_id={2})".format(
            self.id,
            self.addr,
            self.jail_id,
        )
