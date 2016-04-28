"""
WSGI config for workatolist project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


# If, for some reason, it's necessary to deploy the project locally
# with uWSGI, it will ensure that it will work
settings = "workatolist.settings.production"
try:
    with open("settings") as file:
        settings = file.read()
except:
    pass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

application = get_wsgi_application()
