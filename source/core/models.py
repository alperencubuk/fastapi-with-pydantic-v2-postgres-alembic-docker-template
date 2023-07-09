from sqlalchemy import Column, DateTime, Integer, func

from source.core.database import Base


class TimeStampMixin:
    create_date = Column(name="create_date", type_=DateTime, default=func.now())
    update_date = Column(
        name="update_date",
        type_=DateTime,
        default=func.now(),
        onupdate=func.now(),
    )


class Model(TimeStampMixin, Base):
    __abstract__ = True

    id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True)
