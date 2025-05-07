from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from app.models.user import User
from app.schemas.user import UserCreate


async def get(db_session: AsyncSession, user_id: int) -> Optional[User]:
    result = await db_session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_by_email(db_session: AsyncSession, email: str | EmailStr) -> Optional[User]:
    result = await db_session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create(db_session: AsyncSession, user_in: UserCreate) -> User:
    user = User(email=user_in.email, login=user_in.login)
    user.set_password(user_in.password)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
