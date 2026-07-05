from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class TransactionCreate(BaseModel):
    amount: float = Field(gt=0)
    description: str = Field(min_length=1, pattern=r"\S")
    type: Literal["income", "expense"]

class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    type: str
    date: datetime

    class Config:
        from_attributes = True
