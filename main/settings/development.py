from .base import *

DEBUG = True

# add silk to top of middleware
INSTALLED_APPS += ['silk']
MIDDLEWARE.insert(0, 'silk.middleware.SilkyMiddleware')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3'
    }
}
