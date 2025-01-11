# app/database/dynamo_handler.py
import boto3
from datetime import datetime
from typing import Dict, Optional
from ..core.logger import setup_logging

logger = setup_logging()

class DynamoDBHandler:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.transactions_table = self.dynamodb.Table('payment_transactions')
        self.users_table = self.dynamodb.Table('payment_users')

    def save_transaction(self, transaction_data: Dict) -> Dict:
        """Save a new transaction."""
        try:
            item = {
                'transaction_id': transaction_data['transaction_id'],
                'timestamp': int(datetime.now().timestamp()),
                'phone_number': transaction_data['phone_number'],
                'amount': transaction_data['amount'],
                'provider': transaction_data['provider'],
                'status': 'PENDING',
                'currency': 'MWK'
            }
            response = self.transactions_table.put_item(Item=item)
            logger.info(f"Saved transaction: {transaction_data['transaction_id']}")
            return response
        except Exception as e:
            logger.error(f"Error saving transaction: {str(e)}")
            raise

    def update_transaction_status(self, transaction_id: str, status: str) -> Dict:
        """Update transaction status."""
        try:
            response = self.transactions_table.update_item(
                Key={'transaction_id': transaction_id},
                UpdateExpression='SET #status = :status, updated_at = :timestamp',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': status,
                    ':timestamp': int(datetime.now().timestamp())
                },
                ReturnValues="UPDATED_NEW"
            )
            logger.info(f"Updated transaction {transaction_id} status to {status}")
            return response
        except Exception as e:
            logger.error(f"Error updating transaction: {str(e)}")
            raise

    def get_transaction(self, transaction_id: str) -> Optional[Dict]:
        """Get transaction by ID."""
        try:
            response = self.transactions_table.get_item(
                Key={'transaction_id': transaction_id}
            )
            return response.get('Item')
        except Exception as e:
            logger.error(f"Error getting transaction: {str(e)}")
            raise
