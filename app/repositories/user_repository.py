from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import UserModel as User
from app.repositories.base.soft_delete_repository import BaseSoftDeleteRepository


class UserRepository(BaseSoftDeleteRepository):
    model = User

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(self.model, user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(self.model).filter_by(email=email))

    async def update(self, user_id: int, update: dict) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        for field, value in update.items():
            if hasattr(user, field):
                setattr(user, field, value)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        user.delete()
        await self.session.commit()
        return True
