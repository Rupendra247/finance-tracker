from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    amount: float
    description: str
    type: str

class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    type: str
    date: datetime

    class Config:
        from_attributes = True