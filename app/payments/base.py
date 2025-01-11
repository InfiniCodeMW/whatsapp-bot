# app/payments/base.py
from abc import ABC, abstractmethod
from typing import Dict


class BasePaymentProvider(ABC):
    @abstractmethod
    async def initiate_payment(self, phone_number: str, amount: float, reference: str) -> Dict:
        pass

    @abstractmethod
    async def verify_payment(self, reference: str) -> Dict:
        pass

    @abstractmethod
    def verify_callback(self, data: Dict) -> bool:
        pass