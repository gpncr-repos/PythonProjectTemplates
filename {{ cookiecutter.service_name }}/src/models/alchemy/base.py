# stdlib
import uuid

# thirdparty
from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseAlchemyModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[Uuid] = mapped_column(primary_key=True, default=uuid.uuid4())