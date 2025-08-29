from __future__ import annotations

from app.models.base.base_model import ModelMixin
from app.models.base.soft_delete import SoftDeleteMixin

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.teacher_model import TeacherModel

class CourseModel(ModelMixin, SoftDeleteMixin):
    __tablename__ = 'courses'

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)

    teachers: Mapped[list[TeacherModel]] =  relationship(
        'TeacherModel',
        secondary='course_teacher',
        back_populates='courses',
        lazy='selectin'
    )
