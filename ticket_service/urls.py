from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TicketView, TicketDetailsView, CommentView, LikeView

urlpatterns = {
    url(r'^tickets/$', TicketView.as_view()),
    url(r'^tickets/(?P<pk>[0-9]+)/$', TicketDetailsView.as_view()),
    url(r'^comments/$', CommentView.as_view()),
    url(r'^likes/$', LikeView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
