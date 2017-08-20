from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TicketView, SetNeedToConfirmedView, TicketDetailsView, CommentView, CommentDetailsView, LikeView, DislikeView, ContributeView, VoteView, CommentJudgmentView, ChangeStatusView, EditResponsiblesView, EditContributersView

#TODO: set permissions!
urlpatterns = {
    url(r'^tickets/$', TicketView.as_view()),

    url(r'^comments/$', CommentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/$', CommentDetailsView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/judgment$', CommentJudgmentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/like$', LikeView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/dislike$', DislikeView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
