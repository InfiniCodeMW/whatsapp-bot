# app/core/logger.py
import logging
import watchtower
import os


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # CloudWatch handler
    cloudwatch_handler = watchtower.CloudWatchLogHandler(
        log_group='/aws/whatsapp-bot',
        stream_name='application',
        create_log_group=True
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    cloudwatch_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(cloudwatch_handler)
    logger.addHandler(console_handler)
