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

STATIC_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]

