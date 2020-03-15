from .base import *


DEBUG = os.getenv('DEBUG')
STATIC_URL = os.getenv('STATIC_URL')

STATIC_ROOT = os.path.join(BASE_R,  'static')
STATICFILES_DIRS = [
    os.path.join(BASE_R, "staticfiles")

]
MEDIA_ROOT = os.path.join(BASE_R, 'media')

MEDIA_URL = os.getenv('MEDIA_URL')
if os.getenv("postgres"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DBNAME'),  # dbname
            'USER': os.getenv('DBUSER'),
            'PASSWORD': os.getenv('DBPASSWORD'),
            'HOST': os.getenv('DBHOST'),
            'PORT': os.getenv('DBPORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_R, 'db.sqlite3'),
        }
    }
