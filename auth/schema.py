from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserInDB(UserCreate):
    hashed_password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
