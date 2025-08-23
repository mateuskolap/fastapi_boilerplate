from datetime import datetime

from sqlalchemy import ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import table_registry


@table_registry.mapped_as_dataclass()
class ModelMixin:
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    created_by: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=True, init=False
    )
    updated_by: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=True, init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False, init=False
    )
