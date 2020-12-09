from canadasocceracademy.settings import *
import dj_database_url


DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, 'static')
