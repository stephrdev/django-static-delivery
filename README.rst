django-static-delivery
======================

.. image:: https://img.shields.io/pypi/v/django-static-delivery.svg
   :target: https://pypi.org/project/django-static-delivery/
   :alt: Latest Version

.. image:: https://github.com/stephrdev/django-static-delivery/workflows/Test/badge.svg?branch=master
   :target: https://github.com/stephrdev/django-static-delivery/actions?workflow=Test
   :alt: CI Status

.. image:: https://codecov.io/gh/stephrdev/django-static-delivery/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/stephrdev/django-static-delivery
   :alt: Coverage Status

.. image:: https://readthedocs.org/projects/django-static-delivery/badge/?version=latest
   :target: https://django-static-delivery.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status


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

A Python 3 interpreter is required in addition to poetry.

.. code-block:: shell

    $ poetry install


Now you're ready to run the tests:

.. code-block:: shell

    $ make tests
