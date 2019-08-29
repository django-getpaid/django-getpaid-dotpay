from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GetpaidDotpayConfig(AppConfig):
    name = "getpaid_dotpay"
    verbose_name = _("Dotpay backend")

    def ready(self):
        from getpaid.registry import registry

        registry.register(self.module)
