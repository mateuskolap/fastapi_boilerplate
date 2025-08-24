from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.base.pagination import Pagination
from app.schemas.validators.password import PasswordStr
from app.schemas.validators.phone_number import PhoneNumberStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: PhoneNumberStr


class UserCreate(UserBase):
    model_config = ConfigDict(extra='forbid')

    password: PasswordStr


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str | None = None
    email: EmailStr | None = None
    phone: PhoneNumberStr | None = None
    password: PasswordStr | None = None


class User(UserBase):
    pass


class UserRead(User):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
    created_by: int | None
    updated_by: int | None


class UserList(Pagination):
    users: list[UserRead]
