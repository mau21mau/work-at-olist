from workatolist.settings.base import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'olist',
        'NAME': 'workatolist',
        'PASSWORD': 'master',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
