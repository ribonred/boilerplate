from .base import *  # noqa
from .extension import LocalConfig

config = LocalConfig()

INSTALLED_APPS.extend(config.ADDITIONAL_APPS)  # noqa

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },
    "machina_attachments": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/tmp",
    },
}
