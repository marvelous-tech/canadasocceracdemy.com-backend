import os
from datetime import timedelta

import braintree
import storages.backends.s3boto3
from django.conf import settings

import dotenv
dotenv.read_dotenv()

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
                "visualblocks", "code", "fullscreen", "insertdatetime", "mdeia", "table", "paste", "help", "wordcount",
                ],
    'toolbar': "formatselect | fontselect | bold italic strikethrough forecolor backcolor formatpainter | alignleft aligncenter alignright alignjustify | numlist bullist outdent indent | link insertfile image | removeformat | code | addcomment | checklist | casechange",
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

TOKEN_EXPIRATION_TIMEDELTA = timedelta(days=1)

E_LEARNING_PLATFORM = 'http://localhost:7000/e-learning/'
REGISTRATION_PLATFORM = 'http://localhost:4200/registration/'

DEC_LOADER = "disposable_email_checker.emails.email_domain_loader"

SERVER = 'http://127.0.0.1:8000'

if settings.ON_UPLOADED:
    E_LEARNING_PLATFORM = 'https://website.canadasocceracademy.com/e-learning/'
    REGISTRATION_PLATFORM = 'https://website.canadasocceracademy.com/registration/'
    SERVER = 'https://website.canadasocceracademy.com'
