import typing as ty

from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry: ty.Dict = {}  # type: ignore [type-arg]


@as_declarative(class_registry=class_registry)
class Base:
    id: ty.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805 first argument self
        return cls.__name__.lower()
