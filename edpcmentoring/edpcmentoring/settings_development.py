"""
Django configuration for development server.

This configuration inherits values from settings.

"""
# pylint: disable=wildcard-import,unused-wildcard-import
from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5jzqc@zsm=a+ft84=k483ny=3v#=c6p3q&#-$q3ljn-g$5fu0r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
