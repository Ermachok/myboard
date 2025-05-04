from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from sqlalchemy import Column, Integer, String, LargeBinary

from app.core.config import JWT_ALG, JWT_EXP, JWT_SECRET
from app.db.base import Base


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    login = Column(String, unique=True)
    password = Column(LargeBinary, nullable=False)

    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches stored hash"""
        if not password or not self.password:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), self.password)

    def set_password(self, password: str) -> None:
        """Set a new password"""
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = hash_password(password)

    @property
    def token(self):
        now = datetime.utcnow()
        exp = (now + timedelta(seconds=JWT_EXP)).timestamp()
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALG)
