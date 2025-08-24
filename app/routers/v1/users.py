from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserList, UserRead, UserUpdate
from app.security.password_hasher import get_hashed_password

router = APIRouter(prefix='/users', tags=['users'])


def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)


UserRepo = Annotated[UserRepository, Depends(get_user_repository)]



@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def list_users(
    user_repo: UserRepo,
    *,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
    offset: Annotated[int, Query(ge=0)] = 0,
    email: Annotated[str | None, Query()] = None,
    name: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[str, Query(pattern='^(active|inactive|all)$')] = 'active',
):
    filters = {}
    if email:
        filters['email'] = email
    if name:
        filters['name'] = name
    if phone:
        filters['phone'] = phone
    filters['status'] = status

    total = await user_repo.count(filters)
    users = await user_repo.list(limit, offset, filters)

    return UserList(
        total=total, limit=limit, offset=offset, count=len(users), users=users
    )


@router.get('/id/{user_id}', status_code=HTTPStatus.OK, response_model=UserRead)
async def get_user_by_id(user_repo: UserRepo, user_id: int):
    user = await user_repo.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return user


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserRead)
async def create_user(
    user_repo: UserRepo,
    user_in: UserCreate,
):
    if await user_repo.get_by_email(str(user_in.email)):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Email already registered'
        )

    user = UserModel(
        **user_in.model_dump(exclude={'password'}),
        password=get_hashed_password(user_in.password),
    )

    return await user_repo.create(user)


@router.patch(
    '/id/{user_id}', status_code=HTTPStatus.OK, response_model=UserRead
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    repo: UserRepo,
):
    update_data = user_update.model_dump(exclude_unset=True)

    if 'password' in update_data:
        update_data['password'] = get_hashed_password(update_data['password'])

    if 'email' in update_data:
        if await repo.get_by_email(update_data['email']):
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    updated_user = await repo.update(user_id, update_data)

    if not updated_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return updated_user


@router.delete('/id/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int, repo: UserRepo):
    deleted = await repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
