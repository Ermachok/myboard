from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserLoginResponse, UserOut
from app.services.user import (check_user_uniqueness, create, get_by_email,
                               get_current_user)

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_session)):
    await check_user_uniqueness(db, user_in.email, user_in.login)
    user = await create(db_session=db, user_in=user_in)
    return user


@user_router.post("/login", response_model=UserLoginResponse)
async def login_user(user_in: UserLogin, db: AsyncSession = Depends(get_session)):
    user = await get_by_email(db_session=db, email=user_in.email)
    if not user or not user.verify_password(user_in.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(data={"sub": user.email})
    return {"token": token, "email": user.email}


@user_router.get(
    "/me", response_model=UserOut, dependencies=[Depends(get_current_user)]
)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
