from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from ticket_service.tickets.views import (
    TicketView,
    PrivateTicketView,
)
from ticket_service.tickets.attachments.views import (
    PublicAttachmentsView,
    PrivateAttachmentView,
)
from ticket_service.users.views import (
    ProfilePicUploadView,
    PublicProfileView,
)
from ticket_service.tickets.comments.views import (
    CommentView,
    CommentDetailsView,
    CommentJudgmentView,
    LikeView,
    DislikeView
)

#TODO: set permissions!
urlpatterns = {
    url(r'^tickets/$', TicketView.as_view()),
    url(r'^comments/$', CommentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/$', CommentDetailsView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/judgment$', CommentJudgmentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/like$', LikeView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/dislike$', DislikeView.as_view()),
    url(r'^PublicAttachments/$', PublicAttachmentsView.as_view()),
    url(r'^PrivateAttachments/$', PrivateAttachmentView.as_view()),
    url(r'^ProfilePicUpload/(?P<pk>[0-9]+)/$', ProfilePicUploadView.as_view()),
    url(r'^PublicProfile/$', PublicProfileView.as_view()),
    url(r'^PublicProfile/$', PublicProfileView.as_view()),
    url(r'^PrivateTicket/$', PrivateTicketView.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)
