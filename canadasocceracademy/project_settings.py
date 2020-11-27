import os

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'marvelous-tech'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'

AWS_DEFAULT_ACL = 'public-read'

STATIC_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'static')
MEDIA_URL = '{}/{}/'.format(AWS_S3_ENDPOINT_URL, 'media')
