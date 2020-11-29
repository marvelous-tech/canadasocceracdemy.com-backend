import os

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'marvelous-tech'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'
AWS_S3_CUSTOM_DOMAIN = 'marvelous-tech.nyc3.cdn.digitaloceanspaces.com'

AWS_DEFAULT_ACL = 'public-read'

MEDIA_URL = '{}/{}/'.format('https://marvelous-tech.nyc3.cdn.digitaloceanspaces.com', 'media')

TINYMCE_DEFAULT_CONFIG = {
    'plugins': ["lists", "advlist", "link", "image", "charmap", "print", "preview", "anchor", "searchreplace",
                "visualblocks", "code", "fullscreen", "insertdatetime", "mdeia", "table", "paste", "help", "wordcount",
                ],
    'toolbar': "formatselect | fontselect | bold italic strikethrough forecolor backcolor formatpainter | alignleft aligncenter alignright alignjustify | numlist bullist outdent indent | link insertfile image | removeformat | code | addcomment | checklist | casechange",
    'height': 360
}
