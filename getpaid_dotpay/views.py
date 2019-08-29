import swapper
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

Payment = swapper.load_model("getpaid", "Payment")


class DotpayReturnView(View):
    def get(self, request, pk, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=pk)
        status = request.GET.get("status")
        if status is not None:
            if status == "OK":
                payment.change_status("accepted_for_proc")
            else:
                payment.change_status("cancelled")
        return HttpResponseRedirect(payment.order.get_redirect_url())
