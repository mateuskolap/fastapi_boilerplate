from __future__ import annotations

from app.models.base.base_model import ModelMixin
from app.models.base.soft_delete import SoftDeleteMixin

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TeacherModel(ModelMixin, SoftDeleteMixin):
    __tablename__ = 'teachers'

    courses: Mapped[list[TeacherModel]] =  relationship(
        'TeacherModel',
        secondary='course_teacher',
        back_populates='courses',
        lazy='selectin'
    )