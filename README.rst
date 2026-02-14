.. warning::

    **This package has been discontinued.**

=====================
django-getpaid-dotpay
=====================

This package is no longer maintained. Dotpay has **closed down their services
after merging with Przelewy24**. If you were using Dotpay, you should migrate
to the Przelewy24 gateway using the new ``python-getpaid`` ecosystem.

Migration
=========

Replace ``django-getpaid-dotpay`` with the following packages:

1. `python-getpaid-core <https://pypi.org/project/python-getpaid-core/>`_ —
   framework-agnostic payment processing library
2. `django-getpaid <https://pypi.org/project/django-getpaid/>`_ — Django
   framework adapter
3. `python-getpaid-przelewy24 <https://pypi.org/project/python-getpaid-przelewy24/>`_ —
   Przelewy24 gateway plugin (successor to Dotpay)

.. code-block:: shell

    pip install python-getpaid-core django-getpaid python-getpaid-przelewy24

For more information, visit the
`python-getpaid GitHub organization <https://github.com/django-getpaid>`_.

License
=======

MIT
