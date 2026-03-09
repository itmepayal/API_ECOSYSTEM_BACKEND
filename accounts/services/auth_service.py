from django.conf import settings
from accounts.models import User
from core.email.send_email import send_email


class AuthService:

    @staticmethod
    def register_user(email, username, password):

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

        raw_token = user.generate_token(
            token_field="email_verification_token",
            expiry_field="email_verification_expiry",
            expiry_minutes=10
        )

        verify_link = f"{settings.FRONTEND_URL}/verify-email/{raw_token}"

        send_email(
            to_email=user.email,
            subject="Verify your email",
            template_id=settings.SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID,
            dynamic_data={
                "username": user.username,
                "verification_code": raw_token,
                "verify_link": verify_link
            }
        )

        return user