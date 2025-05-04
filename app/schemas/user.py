from pydantic import BaseModel, EmailStr, Field, field_validator


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


class UserRead(UserBase):
    id: int
    login: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    login: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Password must not be empty")
        return v


class UserLoginResponse(BaseModel):
    token: str
    email: EmailStr

    class Config:
        orm_mode = True
