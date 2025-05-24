from pydantic import BaseModel, EmailStr, Field


class ORMBase(BaseModel):
    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "login": "johndoe",
                "password": "StrongPass123",
            }
        }


class UserRead(UserBase, ORMBase):
    id: int
    login: str


class UserOut(UserRead):
    pass


class UserLogin(UserBase):
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "StrongPass123",
            }
        }


class UserLoginResponse(ORMBase):
    token: str
    email: EmailStr
