
from django.conf import settings


ROOT_DIR = getattr(settings, "ROOT_DIR", None)
IMAGE_CACHE_DIR = getattr(settings, "IMAGE_CACHE_DIR", None)
COMPILE_DIR = getattr(settings, "COMPILE_DIR", None)
BLENDED_DIR = getattr(settings, "BLENDED_DIR", None)
SRC = getattr(settings, "SRC", None)
CURRENT_ACCOUNT = getattr(settings, "CURRENT_ACCOUNT", None)
BASE_DIR = getattr(settings, "BASE_DIR", None)

PACKAGE_NAME = getattr(settings, "PACKAGE_NAME", None)

