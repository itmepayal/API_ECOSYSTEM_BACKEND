# =========================================================
# Accounts Models
# =========================================================
from accounts.models import User

# =========================================================
# GET USER BY EMAIL
# =========================================================
def get_user_by_email(email: str):
    if not email:
        return None
    return User.objects.filter(email__iexact=email).first()
