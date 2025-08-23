from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.database import table_registry


@table_registry.mapped_as_dataclass()
class SoftDeleteMixin:
    __abstract__ = True

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, init=False, default=None
    )

    def delete(self):
        self.deleted_at = datetime.now()

    def restore(self):
        self.deleted_at = None

    @property
    def is_deleted(self):
        return self.deleted_at is not None
