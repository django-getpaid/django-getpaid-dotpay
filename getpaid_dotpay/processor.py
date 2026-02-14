import hashlib
from decimal import Decimal
from urllib.parse import urljoin

from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.utils.http import urlencode

from getpaid import PaymentStatus
from getpaid.processor import BaseProcessor

INCOMING_FIELDS = [
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
OUTGOING_FIELDS = [
    "pin",
    "api_version",
    "lang",
    "id",
    "pid",
    "amount",
    "currency",
    "description",
    "control",
    "channel",
    "credit_card_brand",
    "ch_lock",
    "channel_groups",
    "onlinetransfer",
    "url",
    "type",
    "buttontext",
    "urlc",
    "firstname",
    "lastname",
    "email",
    "street",
    "street_n1",
    "street_n2",
    "state",
    "addr3",
    "city",
    "postcode",
    "phone",
    "country",
    "code",
    "p_info",
    "p_email",
    "n_email",
    "expiration_date",
    "deladdr",
    "recipient_account_number",
    "recipient_company",
    "recipient_first_name",
    "recipient_last_name",
    "recipient_address_street",
    "recipient_address_building",
    "recipient_address_apartment",
    "recipient_address_postcode",
    "recipient_address_city",
    "application",
    "application_version",
    "warranty",
    "bylaw",
    "personal_data",
    "credit_card_number",
    "credit_card_expiration_date_year",
    "credit_card_expiration_date_month",
    "credit_card_security_code",
    "credit_card_store",
    "credit_card_store_security_code",
    "credit_card_customer_id",
    "credit_card_id",
    "blik_code",
    "credit_card_registration",
    "surcharge_amount",
    "surcharge",
    "ignore_last_payment_channel",
    "vco_call_id",
    "vco_update_order_info",
    "vco_subtotal",
    "vco_shipping_handling",
    "vco_tax",
    "vco_discount",
    "vco_gift_wrap",
    "vco_misc",
    "vco_promo_code",
    "credit_card_security_code_required",
    "credit_card_operation_type",
    "credit_card_avs",
    "credit_card_threeds",
    "customer",
    "gp_token",
    "blik_refusenopayid",
    "auto_reject_date",
    "ap_token",
]


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
    production_url = "https://ssl.dotpay.pl/t2/"
    sandbox_url = "https://ssl.dotpay.pl/test_payment/"

    def get_paywall_params(self, request):
        extra_args = {}
        channel_groups = self.get_setting("channel_groups")
        channel = self.get_setting("channel")
        flow_type = self.get_setting("type", 0)
        if channel_groups:
            extra_args["channel_groups"] = channel_groups
        elif channel:
            extra_args["channel"] = channel

        email = self.payment.order.get_user_info().get("email")
        if email is not None:
            extra_args["email"] = email

        params = dict(
            pin=self.get_setting("pin"),
            id=self.get_setting("seller_id"),
            api_version="dev",
            amount=self.payment.amount.quantize(Decimal(".01")),
            currency=self.payment.currency.upper(),
            description=self.payment.description,
            lang=self.get_setting("lang") or "en",
            type=flow_type,
            control=str(self.payment.pk),
            url=self.get_return_url(request),
            urlc=request.build_absolute_uri(
                reverse("getpaid:callback-detail", kwargs=dict(pk=self.payment.pk))
            ),
            **extra_args,
        )

        params["chk"] = self.calc_signature(params, OUTGOING_FIELDS)

        return params

    def get_paywall_url(self, params=None):
        base_url = self.get_paywall_baseurl()
        return urljoin(base_url, urlencode(params))

    def get_return_url(self, request):
        return request.build_absolute_uri(
            reverse(
                "getpaid:{}:return-view".format(self.slug),
                kwargs=dict(pk=self.payment.pk),
            )
        )

    def calc_signature(self, data, fields):
        values = tuple(data.get(field, "") for field in fields)
        return hashlib.sha256("".join(values).encode("utf-8")).hexdigest()

    def handle_paywall_callback(self, request, *args, **kwargs):
        data = request.POST

        self.context["external_id"] = data.get("operation_number", "")
        signature = data.get("signature", "")
        control = data.get("control", "")
        status = data.get("operation_status", "")

        checksum = self.calc_signature(data, INCOMING_FIELDS)

        if checksum != signature:
            return HttpResponseBadRequest("BAD SIGNATURE")
        if control != str(self.payment.pk):
            return HttpResponseBadRequest("BAD CONTROL")
        if self.payment.status not in [PaymentStatus.PAID, PaymentStatus.FAILED]:
            if status == "completed":
                self.payment.on_success()
            elif status == "rejected":
                self.payment.on_failure()
            else:
                self.payment.change_status("in_progress")
        return HttpResponse("OK")
