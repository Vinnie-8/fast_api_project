from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str
    created_at: datetime
   
    
    model_config = {"from_attributes": True}
    
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True
        
class NoteCreate(BaseModel):  
    title: str
    content: str
    published:bool = True
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
class NoteResponse(BaseModel): 
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
class TokenData(BaseModel):
    username: Optional[str] = None