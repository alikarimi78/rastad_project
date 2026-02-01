import os  # noqa

from .base import *  # noqa

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", " ").split()

CORS_ORIGIN_ALLOW_ALL = True
