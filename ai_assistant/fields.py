import base64
import hashlib

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models


def _get_fernet() -> Fernet:
    key = base64.urlsafe_b64encode(
        hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    )
    return Fernet(key)


class EncryptedCharField(models.TextField):
    """
    Stores values encrypted with Fernet (AES-128-CBC + HMAC) derived from SECRET_KEY.
    Transparent encrypt/decrypt — treat like a regular CharField.
    """

    def from_db_value(self, value, expression, connection):
        if not value:
            return value
        try:
            return _get_fernet().decrypt(base64.b64decode(value)).decode()
        except Exception:
            return value

    def get_prep_value(self, value):
        if not value:
            return value
        encrypted = _get_fernet().encrypt(value.encode())
        return base64.b64encode(encrypted).decode()

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs
