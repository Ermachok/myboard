from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from sqlalchemy import Column, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from config import JWT_ALG, JWT_EXP, JWT_SECRET


def hash_password(password: str):
    pw = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)

    def verify_password(self, password: str) -> bool:
        if not password or not self.password:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def set_password(self, password: str) -> None:
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = hash_password(password)

    def generate_token(self) -> str:
        now = datetime.now()
        payload = {
            "sub": self.login,
            "email": self.email,
            "exp": now + timedelta(seconds=JWT_EXP),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

    tasks = relationship("Task", back_populates="assigned_user")
    boards = relationship("Board", back_populates="owner")
