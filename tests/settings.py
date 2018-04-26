import os


DEBUG = True

SECRET_KEY = 'testing'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
