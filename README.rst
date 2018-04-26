django-static-delivery
======================

.. image:: https://img.shields.io/pypi/v/django-static-delivery.svg
   :target: https://pypi.python.org/pypi/django-static-delivery
   :alt: Latest Version

.. image:: https://codecov.io/gh/moccu/django-static-delivery/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/moccu/django-static-delivery
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-static-delivery/badge/?version=latest
   :target: https://django-static-delivery.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://travis-ci.org/moccu/django-static-delivery.svg?branch=master
   :target: https://travis-ci.org/moccu/django-static-delivery

Usage
-----

Please refer to the `Documentation <https://django-static-delivery.readthedocs.io/>`_ to
learn how to use ``django-static-delivery``. Basicly, ``static_delivery`` provides a
middleware to serve static files in - for example - Docker setups. The package uses
a middleware instead of a view to make sure we can bypass cookies.


Requirements
------------

django-static-delivery supports Python 3 only and requires at least Django 1.11.
No other dependencies are required.


Prepare for development
-----------------------

A Python 3.6 interpreter is required in addition to pipenv.

.. code-block:: shell

    $ pipenv install --python 3.6
    $ pipenv shell
    $ pip install -e .


Now you're ready to run the tests:

.. code-block:: shell

    $ pipenv run py.test
