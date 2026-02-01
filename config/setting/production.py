import os  # noqa

from .base import *  # noqa

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", " ").split()

CORS_ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS").split()
