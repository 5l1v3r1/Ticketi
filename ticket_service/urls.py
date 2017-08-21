from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
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
from ticket_service.tickets.views import (
    TicketView,
    PrivateTicketView,
    DraftTicketView,
    DraftTicketDetailsView,
    PublishDestroyTicketView,
    TicketDetailsView,
    ContributeView,
    EditContributersView,
    EditResponsiblesView,
    EditResponsiblesPrivateView,
    VoteView,
    ChangeStatusView,
    SetNeedToConfirmedView,
    PrivateTickettDetailsSerializer,
)

#TODO: set permissions!
urlpatterns = {

    url(r'^tickets$', TicketView.as_view()), #TODO: chera details esh asan estefade nashode?!

    url(r'^draft_tickets$', DraftTicketView.as_view()),
    url(r'^draft_tickets/(?P<ticket_id>[0-9]+)$', DraftTicketDetailsView.as_view()),
    url(r'^draft_tickets/(?P<ticket_id>[0-9]+)/publish_or_delete$', PublishDestroyTicketView.as_view()),

    url(r'^PrivateTicket$', PrivateTicketView.as_view()),
    url(r'^PrivateTicket/(?P<private_ticket_id>[0-9]+)$', PrivateTickettDetailsSerializer.as_view()),
    url(r'^PrivateTicket/(?P<private_ticket_id>[0-9]+)/edit_responsibles$', EditResponsiblesPrivateView.as_view()),

    url(r'^tickets/(?P<ticket_id>[0-9]+)$', TicketDetailsView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/contribute$', ContributeView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/edit_contributes$', EditContributersView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/edit_responsibles$', EditResponsiblesView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/vote$', VoteView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/change_status$', ChangeStatusView.as_view()),
    url(r'^tickets/(?P<ticket_id>[0-9]+)/set_need_to_confirmed$', SetNeedToConfirmedView.as_view()),

    url(r'^comments$', CommentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)$', CommentDetailsView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/judgment$', CommentJudgmentView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/like$', LikeView.as_view()),
    url(r'^comments/(?P<comment_id>[0-9]+)/dislike$', DislikeView.as_view()),
    
    url(r'^PublicAttachments$', PublicAttachmentsView.as_view()),
    url(r'^PrivateAttachments$', PrivateAttachmentView.as_view()),
    url(r'^ProfilePicUpload/(?P<pk>[0-9]+)$', ProfilePicUploadView.as_view()),
    url(r'^PublicProfile$', PublicProfileView.as_view()),
    url(r'^PublicProfile$', PublicProfileView.as_view()),

    url(r'^silk/', include('silk.urls', namespace='silk')),
}

urlpatterns = format_suffix_patterns(urlpatterns)
