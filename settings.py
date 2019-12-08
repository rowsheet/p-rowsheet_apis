import os
import django_heroku 
import dj_database_url
import dotenv
from rowsheet.env import PARSE_ENV

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# @TODO change secret key.
SECRET_KEY = "CHANGE_ME!!!! (P.S. the SECRET_KEY environment variable will be used, if set, instead)."

# required BOOL, default False.
DEBUG = PARSE_ENV("DEBUG", os.getenv("DEBUG"), data_type="bool",
        default=False, required=True)

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = [
    "homobiles.herokuapp.com",
    "rideshare.rowsheet.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rowsheet",         # Core application.
    "api",              # API config and entrypoints.
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "rowsheet/templates"),
            os.path.join(BASE_DIR, "rowsheet/templates", "allauth"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {}
DATABASES["default"] = dj_database_url.config(conn_max_age=600)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


django_heroku.settings(locals())
del DATABASES["default"]["OPTIONS"]["sslmode"]


#-------------------------------------------------------------------------------
# ALL-AUTH.
#-------------------------------------------------------------------------------

INSTALLED_APPS += [
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
]
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
LOGIN_REDIRECT_URL = "/set_nonce"
ACCOUNT_LOGOUT_REDIRECT_URL = "/logout_callback"
SITE_ID = 1
WEBAPP_URL = "http://localhost:5003"

#-------------------------------------------------------------------------------
# DEPLOYMENT VARIABLES.
#-------------------------------------------------------------------------------

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

#-------------------------------------------------------------------------------
# API SPEC.
#-------------------------------------------------------------------------------
api_spec_file_path = os.path.join(BASE_DIR, "api.spec")
if os.path.isfile(api_spec_file_path):
    with open(api_spec_file_path, "r") as api_spec_file:
        API_SPEC = api_spec_file.read()
else:
    print("------------------NO API SPEC")
    print(BASE_DIR)


class AuthNonce:
    def __init__(self):
        self.pairs = {}
    def set(self, nonce, session_id):
        self.pairs[nonce] = session_id
    def get(self, nonce):
        session_id = self.pairs.get(nonce)
        if session_id is not None:
            self.pairs.pop(nonce)
        return session_id

AUTH_NONCE = AuthNonce()
