import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # AWS Settings
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

    # DynamoDB Tables
    DYNAMODB_TRANSACTIONS_TABLE = 'payment_transactions'
    DYNAMODB_USERS_TABLE = 'payment_users'

    # WhatsApp Settings
    WHATSAPP_API_VERSION = 'v17.0'
    WHATSAPP_BASE_URL = 'https://graph.facebook.com'

    # Payment Provider Settings
    AIRTEL_API_URL = os.getenv('AIRTEL_API_URL')
    TNM_API_URL = os.getenv('TNM_API_URL')

    # App Settings
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    TESTING = os.getenv('TESTING', 'False') == 'True'