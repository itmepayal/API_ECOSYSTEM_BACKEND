from accounts.models import User

# ---------------------------------
# SELECTOR: GET USER BY EMAIL
# ---------------------------------
def get_user_by_email(email: str):
    return User.objects.filter(email=email).first()