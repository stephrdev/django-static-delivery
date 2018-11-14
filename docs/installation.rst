Installation
============

django-static-delivery supports Python 3 only and requires at least Django 1.11.
No other dependencies are required.

To start, simply install the latest stable package using the command

.. code-block:: shell

    $ pip install django-static-delivery


In addition, you have to add ``'static_delivery.StaticDeliveryMiddleware'``
to the ``MIDDLEWARE`` setting in your ``settings.py``. Make sure to add the middleware
to the top of the list.

.. code-block:: python

    MIDDLEWARE = [
        'static_delivery.StaticDeliveryMiddleware',
        # ... all other middlewares
    ]

Please make sure that your ``staticfiles`` related settings are configured properly.
Besides having ``STATIC_ROOT`` and ``STATIC_URL`` set, you have to use a staticfile
storage with hashed file names, for example ``ManifestStaticFilesStorage``.

.. code-block:: python

    # Filesystem path there collected staticfiles are stored
    STATIC_ROOT = '/var/www/static'

    # Public base path to access files in STATIC_ROOT
    STATIC_URL = '/static/'

    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


Thats it, now continue to the :doc:`Advanced topics section <advanced>` to learn
how to optimize your reverse proxy for a good performance - serving static files
via Django is never a fast way.
