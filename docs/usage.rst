=====
Usage
=====

To use Getpaid-Dotpay in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'getpaid_dotpay.apps.GetpaidDotpayConfig',
        ...
    )

Add Getpaid-Dotpay's URL patterns:

.. code-block:: python

    from getpaid_dotpay import urls as getpaid_dotpay_urls


    urlpatterns = [
        ...
        url(r'^', include(getpaid_dotpay_urls)),
        ...
    ]
