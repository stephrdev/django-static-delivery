Usage
=====

Configuration
-------------

To configure the middleware follow the steps below.

1) Add the middleware to the middleware section in the django settings file.

.. code:: python

    MIDDLEWARE = [
        'static_delivery.StaticDeliveryMiddleware',
        'The rest of your middleware'
    ]

2) Add the following configuration to the settings file of your project

.. code:: python

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'

    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

3) Run python manage command to collect static files and build json manifest.

.. code:: bash

    python manage.py collectstatic

Notes
-----
.. note::

    TODO: Nginx configuration example and additional notes on how to use.
