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

Thats it, now continue to the :doc:`Usage section <usage>` to learn how to optimize
your reverse proxy for a good performance - serving static files via Django is never
a fast way.
