import os
from .secret import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODERATOR_ROOT = os.path.join(BASE_DIR, "moderator")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
    "192.168.1.21"
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "social_django",
    "django_celery_results",
    "othello.apps",
    "othello.apps.auth.apps.AuthConfig",
    "othello.apps.games.apps.GamesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware"
]

ROOT_URLCONF = "othello.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ]
        },
    }
]

ASGI_APPLICATION = 'othello.routing.application'
WSGI_APPLICATION = "othello.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}


# Authentication
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = ("othello.apps.auth.oauth.IonOauth2",)

if DEBUG:
    AUTH_PASSWORD_VALIDATORS = []
    AUTHENTICATION_BACKENDS += ("django.contrib.auth.backends.ModelBackend",)

SOCIAL_AUTH_USER_FIELDS = ["username", "first_name", "last_name", "email", "id"]

SOCIAL_AUTH_URL_NAMESPACE = "social"

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "othello.apps.auth.oauth.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
)

SOCIAL_AUTH_ALWAYS_ASSOCIATE = True

AUTH_USER_MODEL = "authentication.User"

SOCIAL_AUTH_LOGIN_ERROR_URL = "/"
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

LOGIN_URL = "auth:login"
LOGIN_REDIRECT_URL = "games:upload"
LOGOUT_REDIRECT_URL = "auth:index"


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_SAVE_EVERY_REQUEST = True

# Celery
CELERY_RESULT_BACKED = "django-db"

CELERY_BROKER_URL = "redis://localhost:6379/1"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "serve")

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

MEDIA_ROOT = os.path.join(BASE_DIR, "submissions")


# Othello Settings
IMPORT_DRIVER = os.path.join(BASE_DIR, "sandboxing", "import_wrapper.py")

JAILEDRUNNER_DRIVER = os.path.abspath(os.path.join(os.path.dirname(BASE_DIR), "run_ai_jailed.py"))

FIREJAIL_PROFILE = os.path.join(BASE_DIR, "sandboxing", "sandbox.profile")
