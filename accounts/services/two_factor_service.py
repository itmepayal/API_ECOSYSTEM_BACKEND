import pyotp
import qrcode
import base64
from io import BytesIO

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from accounts.models import User


class TwoFactorService:

    # =====================================================
    # GENERATE 2FA SETUP
    # =====================================================
    @staticmethod
    def setup_2fa(user):

        secret = pyotp.random_base32()

        user.totp_secret = secret
        user.is_2fa_enabled = False
        user.save(update_fields=["totp_secret", "is_2fa_enabled"])

        otp_uri = pyotp.TOTP(secret).provisioning_uri(
            name=user.email,
            issuer_name="FREEAPI Hub"
        )

        qr = qrcode.make(otp_uri)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        return {
            "qr_code": qr_base64,
            "manual_key": secret
        }

    # =====================================================
    # VERIFY SETUP
    # =====================================================
    @staticmethod
    def verify_setup(user, code):

        if not user.totp_secret:
            raise ValidationError("2FA not initialized")

        totp = pyotp.TOTP(user.totp_secret)

        if not totp.verify(code, valid_window=1):
            raise ValidationError("Invalid or expired code")

        user.is_2fa_enabled = True
        user.save(update_fields=["is_2fa_enabled"])

        return True

    # =====================================================
    # VERIFY LOGIN 2FA
    # =====================================================
    @staticmethod
    def verify_login_2fa(user_id, code):

        user = get_object_or_404(User, id=user_id)

        if not user.is_2fa_enabled:
            raise ValidationError("2FA is not enabled")

        totp = pyotp.TOTP(user.totp_secret)

        if not totp.verify(code, valid_window=1):
            raise ValidationError("Invalid or expired 2FA code")

        return user

    # =====================================================
    # DISABLE 2FA
    # =====================================================
    @staticmethod
    def disable_2fa(user, code):

        if not user.totp_secret:
            raise ValidationError("2FA not enabled")

        totp = pyotp.TOTP(user.totp_secret)

        if not totp.verify(code, valid_window=1):
            raise ValidationError("Invalid code")

        user.is_2fa_enabled = False
        user.totp_secret = None
        user.save(update_fields=["is_2fa_enabled", "totp_secret"])

        return True