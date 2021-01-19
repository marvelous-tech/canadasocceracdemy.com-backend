# from canadasocceracademy.settings import *
import dj_database_url

from canadasocceracademy.settings import *

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_1-1-34/')

STATIC_URL = 'https://silly-murdock-4165a1.netlify.app/'
