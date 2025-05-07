from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


async def get_by_email(
    db_session: AsyncSession, email: str | EmailStr
) -> Optional[User]:
    result = await db_session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create(db_session: AsyncSession, user_in: UserCreate) -> User:
    user = User(email=user_in.email, login=user_in.login)
    user.set_password(user_in.password)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    email = payload["sub"]
    user = await get_by_email(db_session=db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
