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

urlpatterns = {
    url(r'^tickets/$', TicketView.as_view()),
    url(r'^tickets/(?P<pk>[0-9]+)/$', TicketDetailsView.as_view()),
    url(r'^comments/$', CommentView.as_view()),
    url(r'^likes/$', LikeView.as_view()),
    url(r'^PublicAttachments/$', PublicAttachmentsView.as_view()),
    url(r'^PrivateAttachments/$', PrivateAttachmentView.as_view()),
    url(r'^ProfilePicUpload/(?P<pk>[0-9]+)/$', ProfilePicUploadView.as_view()),
    url(r'^PublicProfile/$', PublicProfileView.as_view()),
    url(r'^PublicProfile/$', PublicProfileView.as_view()),
    url(r'^PrivateTicket/$', PrivateTicketView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
