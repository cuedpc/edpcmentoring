"""
Django configuration for running tests.

This configuration builds on the configuration in settings_development.

"""
# pylint: disable=wildcard-import,unused-wildcard-import
from .settings_development import *

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

SECRET_KEY='orefjkdv'
DEBUG = True

AUTHENTICATION_BACKENDS = [
    # 'ucamwebauth.backends.RavenAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]
# A faster hash for test authentication
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]
# Send emails immediately - when testing, hopefully to a file?!
PINAX_NOTIFICATIONS_QUEUE_ALL=False
