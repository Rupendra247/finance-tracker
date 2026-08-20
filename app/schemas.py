from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.models import TransactionType


class UserCreate(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower().strip()


class UserResponse(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}


class TransactionCreate(BaseModel):
    amount: float = Field(gt=0, description="Must be greater than 0")
    description: str = Field(min_length=1, max_length=500, pattern=r"\S")
    type: TransactionType


class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = Field(default=None, min_length=1, max_length=500, pattern=r"\S")
    type: Optional[TransactionType] = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    type: str
    date: datetime

    model_config = {"from_attributes": True}


class TransactionListResponse(BaseModel):
    transactions: list[TransactionResponse]
    total: int
    page: int
    page_size: int


class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    balance: float


class HealthResponse(BaseModel):
    status: str
    database: str
