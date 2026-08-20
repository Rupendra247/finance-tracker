import pytest
from pydantic import ValidationError

from app.schemas import TransactionCreate, UserCreate


# ── TransactionCreate ─────────────────────────────────────────────────────────


def test_transaction_create_accepts_valid_payload() -> None:
    transaction = TransactionCreate(amount=25.0, description="Lunch", type="expense")
    assert transaction.amount == 25.0
    assert transaction.type == "expense"


def test_transaction_create_accepts_income() -> None:
    transaction = TransactionCreate(amount=100.0, description="Salary", type="income")
    assert transaction.type == "income"


@pytest.mark.parametrize(
    "payload",
    [
        {"amount": 0, "description": "Lunch", "type": "expense"},
        {"amount": -10, "description": "Lunch", "type": "expense"},
        {"amount": 25, "description": "   ", "type": "expense"},
        {"amount": 25, "description": "Lunch", "type": "other"},
    ],
)
def test_transaction_create_rejects_invalid_payload(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        TransactionCreate(**payload)


# ── UserCreate ────────────────────────────────────────────────────────────────


def test_user_create_accepts_valid_payload() -> None:
    user = UserCreate(email="user@example.com", password="securepass123")
    assert user.email == "user@example.com"


def test_user_create_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="user@example.com", password="short")


def test_user_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="securepass123")


def test_user_create_normalizes_email() -> None:
    user = UserCreate(email="  USER@Example.COM  ", password="securepass123")
    assert user.email == "user@example.com"
