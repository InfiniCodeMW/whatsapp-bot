# app/core/security.py
import hmac
import hashlib
from functools import wraps
from flask import request, abort
import os


def verify_webhook_signature(data, signature):
    """Verify WhatsApp webhook signature."""
    expected = hmac.new(
        os.getenv('WHATSAPP_WEBHOOK_SECRET').encode(),
        data,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


def require_webhook_signature(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature or not verify_webhook_signature(request.data, signature):
            abort(403)
        return f(*args, **kwargs)

    return decorated_function