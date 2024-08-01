import importlib.metadata as importlib_metadata


try:
    __version__ = importlib_metadata.version('django-static-delivery')
except Exception:
    __version__ = 'HEAD'

from .middleware import StaticDeliveryMiddleware  # noqa
