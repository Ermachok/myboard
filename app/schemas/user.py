from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "login": "johndoe",
                "password": "StrongPass123",
            }
        }


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    id: int
    login: str

    class Config:
        orm_mode = True
