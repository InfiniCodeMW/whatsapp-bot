# app/payments/tnm.py
import requests
import os
import hmac
import hashlib
from datetime import datetime
from typing import Dict
from .base import BasePaymentProvider
from ..core.logger import setup_logging

logger = setup_logging()


class TNMPayment(BasePaymentProvider):
    def __init__(self):
        self.api_key = os.getenv('TNM_API_KEY')
        self.api_secret = os.getenv('TNM_API_SECRET')
        self.api_url = os.getenv('TNM_API_URL')

    def _generate_signature(self, data: str, timestamp: str) -> str:
        """Generate TNM signature."""
        message = f"{data}{timestamp}"
        signature = hmac.new(
            self.api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    async def initiate_payment(self, phone_number: str, amount: float, reference: str) -> Dict:
        """Initiate TNM Mpamba payment."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            payload = {
                "reference": reference,
                "msisdn": phone_number,
                "amount": amount,
                "currency": "MWK",
                "callback_url": f"{os.getenv('BASE_URL')}/payment/callback/tnm"
            }

            signature = self._generate_signature(str(payload), timestamp)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"ApiKey {self.api_key}",
                "Signature": signature,
                "Timestamp": timestamp
            }

            response = requests.post(
                f"{self.api_url}/payment/request",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error initiating TNM payment: {str(e)}")
            raise