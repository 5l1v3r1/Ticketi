from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TicketView, TicketDetailsView, CommentView, LikeView, DislikeView, ContributeView, VoteView

urlpatterns = {
    url(r'^tickets/$', TicketView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/$', TicketDetailsView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/contribute$', ContributeView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/vote$', VoteView.as_view()),

    url(r'^comments/$', CommentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/like$', LikeView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/dislike$', DislikeView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
