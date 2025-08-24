from sqlalchemy import func, select


class BaseSoftDeleteRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def list(self, limit: int, offset: int, filters=None):
        stmt = select(self.model)
        filters = dict(filters) if filters else {}
        status = filters.pop('status', 'active')
        if status == 'active':
            stmt = stmt.filter(self.model.deleted_at.is_(None))
        elif status == 'inactive':
            stmt = stmt.filter(self.model.deleted_at.is_not(None))
        for field, value in filters.items():
            stmt = stmt.filter(getattr(self.model, field) == value)
        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def count(self, filters=None):
        stmt = select(func.count(self.model.id))
        filters = dict(filters) if filters else {}
        status = filters.pop('status', 'active')
        if status == 'active':
            stmt = stmt.filter(self.model.deleted_at.is_(None))
        elif status == 'inactive':
            stmt = stmt.filter(self.model.deleted_at.is_not(None))
        for field, value in filters.items():
            stmt = stmt.filter(getattr(self.model, field) == value)
        result = await self.session.scalar(stmt)
        return result or 0
