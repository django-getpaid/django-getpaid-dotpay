=============================
Getpaid-Dotpay
=============================

.. image:: https://badge.fury.io/py/getpaid-dotpay.svg
    :target: https://badge.fury.io/py/getpaid-dotpay

.. image:: https://travis-ci.org/django-getpaid/getpaid-dotpay.svg?branch=master
    :target: https://travis-ci.org/django-getpaid/getpaid-dotpay

.. image:: https://codecov.io/gh/django-getpaid/getpaid-dotpay/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/django-getpaid/getpaid-dotpay

Dotpay backend for django-getpaid

Documentation
-------------

The full documentation is at https://getpaid-dotpay.readthedocs.io.

Quickstart
----------

Install Getpaid-Dotpay::

    pip install getpaid-dotpay

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'getpaid',
        'getpaid_dotpay',
        ...
    )


Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
