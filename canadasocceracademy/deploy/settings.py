# from canadasocceracademy.settings import *
import dj_database_url

from canadasocceracademy.settings import *





DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATIC_URL = 'https://cdn.jsdelivr.net/gh/marvelous-tech/canadasocceracdemy.com-backend@master/staticfiles/'
