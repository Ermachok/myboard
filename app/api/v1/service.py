from typing import Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get(db_session: Session, user_id: int) -> Optional[User]:
    return db_session.query(User).filter(User.id == user_id).first()


def get_by_email(db_session: Session, email: str | EmailStr) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()


def create(db_session: Session, user_in: UserCreate) -> User:
    user = User(email=user_in.email, login=user_in.login)
    user.set_password(user_in.password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
