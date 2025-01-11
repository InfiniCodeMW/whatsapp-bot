# app/payments/airtel.py
import requests
import os
from datetime import datetime
from typing import Dict
import jwt
from .base import BasePaymentProvider
from ..core.logger import setup_logging

logger = setup_logging()


class AirtelPayment(BasePaymentProvider):
    def __init__(self):
        self.client_id = os.getenv('AIRTEL_CLIENT_ID')
        self.client_secret = os.getenv('AIRTEL_CLIENT_SECRET')
        self.api_url = os.getenv('AIRTEL_API_URL')
        self.access_token = None
        self.token_expires_at = None

    def _get_access_token(self) -> str:
        """Get Airtel Money access token."""
        if self.access_token and self.token_expires_at > datetime.now().timestamp():
            return self.access_token

        try:
            response = requests.post(
                f"{self.api_url}/auth/oauth2/token",
                auth=(self.client_id, self.client_secret),
                data={"grant_type": "client_credentials"}
            )
            response.raise_for_status()
            data = response.json()

            self.access_token = data['access_token']
            self.token_expires_at = datetime.now().timestamp() + data['expires_in']

            return self.access_token
        except Exception as e:
            logger.error(f"Error getting Airtel access token: {str(e)}")
            raise

    async def initiate_payment(self, phone_number: str, amount: float, reference: str) -> Dict:
        """Initiate Airtel Money payment."""
        try:
            headers = {
                "Authorization": f"Bearer {self._get_access_token()}",
                "Content-Type": "application/json"
            }

            payload = {
                "reference": reference,
                "subscriber": {
                    "country": "MWK",
                    "currency": "MWK",
                    "msisdn": phone_number
                },
                "transaction": {
                    "amount": amount,
                    "country": "MWK",
                    "currency": "MWK",
                    "id": reference
                }
            }

            response = requests.post(
                f"{self.api_url}/merchant/v1/payments/",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error initiating Airtel payment: {str(e)}")
            raise
