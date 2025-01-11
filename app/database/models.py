# app/database/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transaction:
    transaction_id: str
    phone_number: str
    amount: float
    provider: str
    status: str
    timestamp: int
    currency: str = 'MWK'
    updated_at: Optional[int] = None

@dataclass
class User:
    phone_number: str
    name: Optional[str]
    created_at: int
    last_transaction: Optional[str]
    total_transactions: int = 0