from .settings import *

DEBUG = True

# MIDDLEWARE.remove('django.middleware.cache.UpdateCacheMiddleware')
# MIDDLEWARE.remove('django.middleware.cache.FetchFromCacheMiddleware')
# del CACHES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # local
        'NAME': 'ewp',
        'USER': 'djangouser',
        'PASSWORD': '12345'
    }
}