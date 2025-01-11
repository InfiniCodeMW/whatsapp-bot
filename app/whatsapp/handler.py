# app/whatsapp/handler.py
from flask import current_app
import requests
from typing import Dict
import json
from ..core.logger import setup_logging

logger = setup_logging()


class WhatsAppHandler:
    def __init__(self):
        self.api_version = 'v17.0'
        self.base_url = 'https://graph.facebook.com'
        self.access_token = current_app.config['WHATSAPP_ACCESS_TOKEN']
        self.phone_number_id = current_app.config['WHATSAPP_PHONE_NUMBER_ID']

    async def send_message(self, to: str, message: str) -> Dict:
        """Send WhatsApp message."""
        try:
            url = f"{self.base_url}/{self.api_version}/{self.phone_number_id}/messages"

            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message}
            }

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logger.info(f"Message sent to {to}")
            return response.json()
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            raise

    def process_message(self, message: Dict) -> Dict:
        """Process incoming WhatsApp message."""
        try:
            message_type = message.get('type')
            sender = message.get('from')

            if message_type == 'text':
                text = message.get('text', {}).get('body', '').lower()
                return self._process_text_message(sender, text)

            return {
                'status': 'error',
                'message': 'Unsupported message type'
            }
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    def _process_text_message(self, sender: str, text: str) -> Dict:
        """Process text message and determine action."""
        if text.startswith('pay'):
            return self._handle_payment_command(sender, text)
        elif text.startswith('balance'):
            return self._handle_balance_command(sender)
        elif text.startswith('help'):
            return self._handle_help_command(sender)
        else:
            return self._handle_unknown_command(sender)

    async def _handle_payment_command(self, sender: str, text: str) -> Dict:
        """Handle payment command."""
        try:
            parts = text.split()
            if len(parts) != 3:
                await self.send_message(
                    sender,
                    "Invalid format. Please use: pay <provider> <amount>\n"
                    "Example: pay airtel 1000"
                )
                return {'status': 'error', 'message': 'Invalid format'}

            _, provider, amount = parts

            if provider not in ['airtel', 'tnm']:
                await self.send_message(
                    sender,
                    "Invalid provider. Please use 'airtel' or 'tnm'"
                )
                return {'status': 'error', 'message': 'Invalid provider'}

            try:
                amount = float(amount)
            except ValueError:
                await self.send_message(
                    sender,
                    "Invalid amount. Please enter a valid number"
                )
                return {'status': 'error', 'message': 'Invalid amount'}

            return {
                'status': 'success',
                'action': 'payment',
                'provider': provider,
                'amount': amount,
                'sender': sender
            }
        except Exception as e:
            logger.error(f"Error handling payment command: {str(e)}")
            raise