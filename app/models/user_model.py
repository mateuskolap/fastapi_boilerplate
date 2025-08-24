from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_declarative_extensions.audit import audit

from app.db.table_registry import table_registry
from app.models.base.base_model import ModelMixin
from app.models.base.soft_delete import SoftDeleteMixin


@audit(ignore_columns={'password', 'created_by', 'created_at'})
@table_registry.mapped_as_dataclass()
class UserModel(ModelMixin, SoftDeleteMixin):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    phone: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
