"""
WSGI config for edpcmentoring project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/

The whitenoise configuration is taken from

    https://devcenter.heroku.com/articles/django-assets

It is what allows the application to serve its own static files in production.

"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edpcmentoring.settings")

application = DjangoWhiteNoise(get_wsgi_application())
