from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.service import create, get_by_email
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserLoginResponse, UserOut

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = get_by_email(db_session=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    user = create(db_session=db, user_in=user_in)
    return user


@user_router.post("/login", response_model=UserLoginResponse)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    user = get_by_email(db_session=db, email=user_in.email)
    if not user or not user.verify_password(user_in.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {"token": user.token, "email": user.email}
