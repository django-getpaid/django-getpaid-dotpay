import hashlib
from decimal import Decimal

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse

from getpaid.processor import BaseProcessor


class PaymentProcessor(BaseProcessor):
    slug = "dotpay"
    display_name = "Dotpay"
    accepted_currencies = [
        "PLN",
        "EUR",
        "USD",
        "GBP",
        "JPY",
        "CZK",
        "SEK",
        "UAH",
        "RON",
    ]
    method = "GET"
    endpoint = "https://ssl.dotpay.pl/t2/"
    sandbox = "https://ssl.dotpay.pl/test_payment/"

    def get_redirect_params(self):
        extra_args = {}
        channel_groups = self.get_setting("channel_groups")
        channel = self.get_setting("channel")
        flow_type = self.get_setting("type")
        if channel_groups:
            extra_args["channel_groups"] = channel_groups
        elif channel:
            extra_args["channel"] = channel

        email = self.payment.order.get_user_info().get("email")
        if email is not None:
            extra_args["email"] = email

        return dict(
            id=self.get_setting("seller_id"),
            amount=self.payment.amount.quantize(Decimal(".01")),
            currency=self.payment.currency.upper(),
            description=self.payment.description,
            lang=self.get_setting("lang") or "en",
            type=flow_type,
            control=str(self.payment.pk),
            URL=self.get_return_url(),
            URLC=reverse("getpaid:callback-detail", kwargs=dict(pk=self.payment.pk)),
            **extra_args,
        )

    def get_redirect_url(self):
        if settings.DEBUG:
            return self.sandbox
        return self.endpoint

    def get_return_url(self):
        return reverse(
            "getpaid:{}:return-view".format(self.slug), kwargs=dict(pk=self.payment.pk)
        )

    def handle_callback(self, request, *args, **kwargs):
        data = request.POST

        self.context["external_id"] = data.get("operation_number", "")

        control = data.get("control", "")
        status = data.get("operation_status", "")
        signature = data.get("signature", "")

        ordered_fields = [
            "id",
            "operation_number",
            "operation_type",
            "operation_status",
            "operation_amount",
            "operation_currency",
            "operation_withdrawal_amount",
            "operation_commission_amount",
            "is_completed",
            "operation_original_amount",
            "operation_original_currency",
            "operation_datetime",
            "operation_related_number",
            "control",
            "description",
            "email",
            "p_info",
            "p_email",
            "credit_card_issuer_identification_number",
            "credit_card_masked_number",
            "credit_card_brand_codename",
            "credit_card_brand_code",
            "credit_card_id",
            "channel",
            "channel_country",
            "geoip_country",
        ]

        values = (
            self.get_setting("pin"),
            *[data.get(field, "") for field in ordered_fields],
        )
        values_hash = hashlib.sha256("".join(values).encode("utf-8")).hexdigest()

        if values_hash != signature:
            return HttpResponseBadRequest("BAD SIGNATURE")
        if control != str(self.payment.pk):
            return HttpResponseBadRequest("BAD CONTROL")
        if self.payment.status not in ["paid", "failed"]:
            if status == "completed":
                self.payment.on_success()
            elif status == "rejected":
                self.payment.on_failure()
            else:
                self.payment.change_status("in_progress")
        return HttpResponse("OK")
