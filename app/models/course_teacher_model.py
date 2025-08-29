from __future__ import annotations

from app.models.base.base_model import ModelMixin
from app.models.base.soft_delete import SoftDeleteMixin

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

class CourseTeacherModel(ModelMixin, SoftDeleteMixin):
    __tablename__ = 'course_teacher'

    course_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('courses.id'), nullable=False, index=True
    )

    teacher_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('teachers.id'), nullable=False, index=True
    )
