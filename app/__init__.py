# app/__init__.py
from flask import Flask
from .config import Config
from .database.dynamo_handler import DynamoDBHandler
from .whatsapp.handler import WhatsAppHandler
from .payments.airtel import AirtelPayment
from .payments.tnm import TNMPayment


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize handlers
    db_handler = DynamoDBHandler()
    whatsapp_handler = WhatsAppHandler()
    airtel_payment = AirtelPayment()
    tnm_payment = TNMPayment()

    # Register blueprints
    from .whatsapp.routes import bp as whatsapp_bp
    from .payments.routes import bp as payments_bp

    app.register_blueprint(whatsapp_bp)
    app.register_blueprint(payments_bp)

    return app
