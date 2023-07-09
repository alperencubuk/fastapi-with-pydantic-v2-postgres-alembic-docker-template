from sqlalchemy import Column, String

from source.core.models import Model


class BoilerplateModel(Model):
    __tablename__ = "Boilerplate"

    email = Column(name="email", type_=String, index=True, unique=True)
    first_name = Column(name="first_name", type_=String, nullable=True)
    last_name = Column(name="last_name", type_=String, nullable=True)
