from django.conf.urls import url

from .views import DotpayReturnView

urlpatterns = [
    url(r"^return/(?P<pk>[0-9a-f-]+)/$", DotpayReturnView.as_view(), name="return-view")
]
