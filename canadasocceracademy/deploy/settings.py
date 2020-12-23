# from canadasocceracademy.settings import *
import dj_database_url

from canadasocceracademy.settings import *





DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_DIRS = None

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

# STATIC_URL = '{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, 'static')

# TINYMCE_JS_URL = 'https://marvelous-tech.nyc3.cdn.digitaloceanspaces.com/tinymce/tinymce.min.js'
