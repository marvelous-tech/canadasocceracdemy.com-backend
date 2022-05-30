"""
Django settings for canadasocceracademy project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import dotenv

dotenv.read_dotenv()

from pathlib import Path
import os
import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import braintree

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY') or 'HEY MAN!!!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.environ.get('DEBUG') == 'false' else True

ON_UPLOADED = False if os.environ.get('ON_UPLOADED') == 'false' else True

HOSTS = os.environ.get('ALLOWED_HOSTS')

ALLOWED_HOSTS = HOSTS.split(',') if HOSTS else []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.join(BASE_DIR, 'logs'), 'app.log'),
            'formatter': 'verbose'
        },
        'app_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.join(BASE_DIR, 'logs'), 'app.log'),
            'formatter': 'verbose'
        },
        'sql_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.join(BASE_DIR, 'logs'), 'sql.log'),
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'qinspect': {
            'handlers': ['sql_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['error_file', 'app_file'],
            'propagate': True,
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'core.middlewares.WwwRedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middlewares.TimezoneMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'qinspect.middleware.QueryInspectMiddleware',
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'canadasocceracademy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'accounts.processors.tags',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'canadasocceracademy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/assets/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets/')
]

# MODULE APPS


INSTALLED_APPS += [
    'debug_toolbar',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'tinymce',
    'rest_auth',
    'django_hosts',
    'private_storage',
    'phonenumber_field',
    'django_q',
    'crispy_forms',
    'chunked_upload',
    # "djstripe",
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

CHUNKED_UPLOAD_PATH = 'chunked_uploads'

CHUNKED_UPLOAD_STORAGE_CLASS = 'django.core.files.storage.FileSystemStorage'

INTERNAL_IPS = ("127.0.0.1", "172.17.0.1")

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://\w+\.canadasocceracademy\.com$",
        "http://localhost:4200"
    ]

#
# # Import REST Framework Settings
#
# try:
#     from canadasocceracademy.rest_settings import *
#     from canadasocceracademy.project_settings import *
# except ImportError as e:
#     print(e)


# APPS

INSTALLED_APPS += [
    'site_data',
    'accounts',
    'comment',
    'e_learning',
    'payments',
    'email_client',
    'studio',
    'stripe_gateway',
    'campaign',
]


def utf8(s: bytes):
    return str(s, 'utf-8')


private_key = ec.generate_private_key(
    ec.SECP521R1(),
    backend=default_backend()
)
public_key = private_key.public_key()

private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

SITE_ID = 1
REST_USE_JWT = True

print(DEBUG)

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=365),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,

}

ROOT_HOSTCONF = 'canadasocceracademy.hosts'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_HOST = "www"

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'marvelous-tech'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_S3_CUSTOM_DOMAIN = 'marvelous-tech.nyc3.cdn.digitaloceanspaces.com'

AWS_DEFAULT_ACL = 'public-read'

# MEDIA_URL = '{}/{}/'.format('https://marvelous-tech.nyc3.cdn.digitaloceanspaces.com', 'media')

TINYMCE_DEFAULT_CONFIG = {
    'plugins': ["lists", "advlist", "link", "image", "charmap", "print", "preview", "anchor", "searchreplace",
                "visualblocks", "code", "fullscreen", "insertdatetime", "media", "table", "paste", "help", "wordcount",
                ],
    'toolbar': "formatselect | fontselect | bold italic strikethrough forecolor backcolor formatpainter | alignleft aligncenter alignright alignjustify | numlist bullist outdent indent | link insertfile image media | removeformat | code | addcomment | checklist | casechange",
    'height': 360
}

# AWS_S3_SIGNATURE_VERSION = 's3v4'
#
# AWS_QUERYSTRING_EXPIRE = '100'

BRAINTREE_MERCHANT_ID = os.environ.get('MID')
BRAINTREE_PRIVATE_KEY = os.environ.get('PRK')
BRAINTREE_PUBLIC_KEY = os.environ.get('PBK')
BRAINTREE_ENVIRONMENT = braintree.Environment.Sandbox \
    if os.environ.get('BEV') == 's' else \
    braintree.Environment.Production

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

TOKEN_EXPIRATION_TIMEDELTA = datetime.timedelta(days=1)

E_LEARNING_PLATFORM = 'http://localhost:7000/e-learning/'
REGISTRATION_PLATFORM = 'http://localhost:4200/registration/'

DEC_LOADER = "disposable_email_checker.emails.email_domain_loader"

SERVER = 'http://127.0.0.1:8000'

if ON_UPLOADED:
    E_LEARNING_PLATFORM = 'https://canadasocceracademy.com/e-learning/'
    REGISTRATION_PLATFORM = 'https://canadasocceracademy.com/registration/'
    SERVER = 'https://canadasocceracademy.com'

"""STRIPE"""

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

STRIPE_TEST_SECRET_KEY = STRIPE_SECRET_KEY
STRIPE_LIVE_MODE = True
DJSTRIPE_WEBHOOK_SECRET = STRIPE_WEBHOOK_SECRET
DJSTRIPE_FOREIGN_KEY_TO_FIELD = 'id'
DJSTRIPE_USE_NATIVE_JSONFIELD = True

FRONTEND_VERSION = 'BE-V1.1.35'

NO_REPLY_MAIL_ADDRESS = os.environ.get('NO_REPLY_MAIL_ADDRESS', 'no-reply@canadasocceracademy.com')
SUPPORT_MAIL_ADDRESS = os.environ.get('SUPPORT_MAIL_ADDRESS', 'support@canadasocceracademy.com')
SUPPORT_PHONE_NUMBER = os.environ.get('SUPPORT_PHONE_NUMBER', '+1 416 201 2425')

QUERY_INSPECT_ENABLED = True
QUERY_INSPECT_LOG_QUERIES = True
