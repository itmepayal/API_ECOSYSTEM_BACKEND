import os
import cloudinary
import cloudinary.api
import dj_database_url
from pathlib import Path
import cloudinary.uploader
from datetime import timedelta
from dotenv import load_dotenv

# -------------------------------------------------
# Base Directory
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------
# Environment Detection
# -------------------------------------------------
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# -------------------------------------------------
# Load ENV file
# -------------------------------------------------
if ENVIRONMENT == "production":
    ENV_PATH = BASE_DIR / ".env"
else:
    ENV_PATH = BASE_DIR / ".env.local"

load_dotenv(ENV_PATH)

# -------------------------------------------------
# Security
# -------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-secret-key")

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
# -------------------------------------------------
# Applications
# -------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "django_filters",

    # Local Apps
    "accounts",
    "api_catalog",
    "playground",
    "request_logs",
]

# -------------------------------------------------
# Middleware
# -------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------------------------------------
# URL Configuration
# -------------------------------------------------
ROOT_URLCONF = "config.urls"

# -------------------------------------------------
# Templates
# -------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -------------------------------------------------
# WSGI
# -------------------------------------------------
WSGI_APPLICATION = "config.wsgi.application"

# -------------------------------------------------
# Database
# -------------------------------------------------
if ENVIRONMENT == "production":
    DATABASES = {
        "default": dj_database_url.parse(
            os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True
        )
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -------------------------------------------------
# Password Validation
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# -------------------------------------------------
# Internationalization
# -------------------------------------------------
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



# -------------------------------------------------
# Custom User Model
# -------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

# -------------------------------------------------
# Django REST Framework
# -------------------------------------------------
REST_FRAMEWORK = {

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    "EXCEPTION_HANDLER":
        "core.exceptions.global_exception_handler.custom_exception_handler",

    "DEFAULT_SCHEMA_CLASS":
        "drf_spectacular.openapi.AutoSchema",

    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],

    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,

    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],

    "DEFAULT_THROTTLE_RATES": {
        # Global
        "anon": "20/min",
        "user": "100/min",

        # Auth APIs
        "auth": "10/min",
        "login": "5/min",
        "register": "5/min",

        # Sensitive
        "resend": "3/min",
        "forgot_password": "3/min",

        # 2FA
        "two_factor": "5/min",
    },
}

# -------------------------------------------------
# JWT Configuration
# -------------------------------------------------
SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_MINUTES", 60))
    ),

    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(os.getenv("REFRESH_TOKEN_DAYS", 7))
    ),

    "AUTH_HEADER_TYPES": ("Bearer",),

    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),

    "ROTATE_REFRESH_TOKENS": True,

    "BLACKLIST_AFTER_ROTATION": True,
}

# -------------------------------------------------
# Email (SendGrid)
# -------------------------------------------------
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

EMAIL_FROM = os.getenv(
    "EMAIL_FROM",
    "noreply@example.com"
)

SENDGRID_PASSWORD_RESET_TEMPLATE_ID = os.getenv(
    "SENDGRID_PASSWORD_RESET_TEMPLATE_ID"
).strip()

SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID = os.getenv(
    "SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID"
).strip()

# -------------------------------------------------
# Frontend URL
# -------------------------------------------------
FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "https://api-ecosystem.vercel.app"
)

# -------------------------------------------------
# CORS
# -------------------------------------------------

CORS_ALLOW_CREDENTIALS = True

if ENVIRONMENT == "development":

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

else:

    CORS_ALLOWED_ORIGINS = [
        FRONTEND_URL,
        "http://localhost:3000",
    ]

CSRF_TRUSTED_ORIGINS = [
    "https://api-ecosystem.vercel.app",
    "http://localhost:3000",
]

# -------------------------------------------------
# OpenAPI / Swagger
# -------------------------------------------------
SPECTACULAR_SETTINGS = {

    "TITLE": "FreeAPI Ecosystem Backend",

    "DESCRIPTION": """
    Production-ready APIs for authentication, e-commerce,
    chat systems, social media features, and utilities.
    Designed for developers to build real-world applications.
    """,

    "VERSION": "1.0.0",

    "SERVE_INCLUDE_SCHEMA": False,

    "SCHEMA_PATH_PREFIX": r"/api/v1/",

    "COMPONENT_SPLIT_REQUEST": True,
}

# -------------------------------------------------
# GOOGLE 
# -------------------------------------------------
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# -------------------------------------------------
# CLOUDINARY 
# -------------------------------------------------
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET,
    secure = True
)

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# -------------------------------------------------
# Static Files
# -------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"