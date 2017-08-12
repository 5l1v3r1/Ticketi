from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TicketView

urlpatterns = {
    url(r'^tickets/$', TicketView.as_view(), name="tickets"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
