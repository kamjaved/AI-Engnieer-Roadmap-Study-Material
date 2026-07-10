from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for every ORM model in this project.

    Kept in its own module rather than defined inline in models.py so that
    anything needing to reference Base without the concrete model classes
    (a future Alembic env.py, a generic repository base) doesn't have to
    import models.py and risk a circular import.
    """
