from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TicketView, TicketDetailsView, CommentView, CommentDetailsView, LikeView, DislikeView, ContributeView, VoteView, CommentJudgmentView

#TODO: set permissions!
urlpatterns = {
    url(r'^tickets/$', TicketView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/$', TicketDetailsView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/contribute$', ContributeView.as_view()),
    # url(r'^tickets/(?P<ticket_id>[0-9]+)/edit_contributes$', VoteView.as_view()),
    # url(r'^tickets/(?P<ticket_id>[0-9]+)/edit_addressed_users$', VoteView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/vote$', VoteView.as_view()),
    # url(r'^tickets/(?P<ticket_id>[0-9]+)/change_status$', VoteView.as_view()),
    # url(r'^tickets/(?P<ticket_id>[0-9]+)/set_need_to_confirmed$', VoteView.as_view()),


    url(r'^comments/$', CommentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/$', CommentDetailsView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/judgment$', CommentJudgmentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/like$', LikeView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/dislike$', DislikeView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
