import pytest
from pydantic import ValidationError

from app.schemas import TransactionCreate


def test_transaction_create_accepts_valid_payload() -> None:
    transaction = TransactionCreate(
        amount=25.0,
        description="Lunch",
        type="expense",
    )
    assert transaction.amount == 25.0


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
