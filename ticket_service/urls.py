from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    TicketView,
    TicketDetailsView,
    CommentView,
    LikeView,
    PublicAttachmentsView,
    PrivateAttachmentView,
    ProfilePicUploadView,
    PublicProfileView,
    PrivateTicketView,
)

#TODO: set permissions!
urlpatterns = {
    url(r'^tickets/$', TicketView.as_view()),

    url(r'^comments/$', CommentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/$', CommentDetailsView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/judgment$', CommentJudgmentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/like$', LikeView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/dislike$', DislikeView.as_view()),

    url(r'^likes/$', LikeView.as_view()),
    url(r'^PublicAttachments/$', PublicAttachmentsView.as_view()),
    url(r'^PrivateAttachments/$', PrivateAttachmentView.as_view()),
    url(r'^ProfilePicUpload/(?P<pk>[0-9]+)/$', ProfilePicUploadView.as_view()),
    url(r'^PublicProfile/$', PublicProfileView.as_view()),
    url(r'^PublicProfile/$', PublicProfileView.as_view()),
    url(r'^PrivateTicket/$', PrivateTicketView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
