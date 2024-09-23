# thirdparty
from sqlalchemy.orm import DeclarativeBase


class BaseAlchemyModel(DeclarativeBase):
    __abstract__ = True
