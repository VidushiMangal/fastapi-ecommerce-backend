from pydantic import BaseModel, EmailStr
from app.common.enums import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    password: str
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True
