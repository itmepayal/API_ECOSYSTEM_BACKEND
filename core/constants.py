# ==========================
# ROLE CONSTANTS
# ==========================
ROLE_ADMIN = "ADMIN"
ROLE_USER = "USER"

ROLE_CHOICES = [
    (ROLE_ADMIN, "Admin"),
    (ROLE_USER, "User"),
]


# ==========================
# LOGIN TYPE CONSTANTS
# ==========================
LOGIN_EMAIL = "EMAIL"
LOGIN_GOOGLE = "GOOGLE"

LOGIN_TYPE_CHOICES = [
    (LOGIN_EMAIL, "Email"),
    (LOGIN_GOOGLE, "Google"),
]