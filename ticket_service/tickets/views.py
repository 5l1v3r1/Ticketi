from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
import datetime

from .models import (
    Ticket,
    PrivateTicket,
)

from .activities.serializers import (
    SetConfirmationLimitActivitySerializer
)

from .activities.models import (
    SetConfirmationLimitActiviy
)

from .serializers import (
    TicketSerializer,
    TicketDetailsSerializer,
    PrivateTicketSerializer,
    ContributeSerializer,
    SetNeedToConfirmedSerializer,
    VoteSerializer,
    ChangeStatusSerializer,
    EditContributersSerializer,
    EditResponsiblesSerializer,
    DraftTicketSerializer,
    DraftTicketDetailsSerializer,
    PublishDestroyTicketSerializer,
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

class DraftTicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.filter(is_draft=True)
    serializer_class = DraftTicketSerializer

    def perform_create(self, serializer):
        serializer.save()

class DraftTicketDetailsView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'

    queryset = Ticket.objects.filter(is_draft=True)
    serializer_class = DraftTicketDetailsSerializer

    # def get_queryset(self):
    #     comment_id = self.kwargs['comment_id']
    #     user = self.request.user
    #     return Like.objects.filter(Q(comment_id=comment_id) & Q(user=user))

class PublishDestroyTicketView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'
    queryset = Ticket.objects.filter(is_draft=True)
    serializer_class = PublishDestroyTicketSerializer

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        ticket.creation_time = datetime.datetime.now()
        ticket.is_draft = False
        serializer.save(ticket=ticket)


class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        parent = serializer.validated_data['parent']
        serializer.save()
        if parent:
            ReopenActivity(
                user = self.request.user,
                ticket = parent,
                new_ticket = Ticket.objects.get(id=serializer.data['id'])
            ).save()

class TicketDetailsView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailsSerializer

    def perform_update(self, serializer):
        ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        EditTicketActivity(
            user = self.request.user,
            ticket = ticket,
            prev_title = ticket.title,
            prev_body = ticket.body
        ).save()
        serializer.save()

class PrivateTicketView(generics.ListCreateAPIView): #TODO: be in aslan niazi nist, vase teste. (chon listo support nemikone -_-)
    queryset = PrivateTicket.objects.all()
    serializer_class = PrivateTicketSerializer

class ContributeView(generics.CreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'

    queryset = Ticket.objects.all()
    serializer_class = ContributeSerializer

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        user = self.request.user
        request_type = serializer.data['request_type']

        ticket.in_list_contributers.remove(user)
        if request_type == 1: # accept
            ticket.contributers.add(user)
        else:   # reject
            pass

class SetNeedToConfirmedView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'

    queryset = Ticket.objects.all()
    serializer_class = SetNeedToConfirmedSerializer

    def perform_update(self, serializer):
        SetConfirmationLimitActiviy(
            user = self.request.user,
            ticket = Ticket.objects.get(id=self.kwargs['ticket_id']),
            need_to_confirmed = serializer.validated_data['need_to_confirmed'],
            limit_value = serializer.validated_data['minimum_approvers_count']
        ).save()
        serializer.save()


class VoteView(generics.CreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'

    queryset = Ticket.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        user = self.request.user
        request_type = serializer.data['request_type']
        vote = serializer.data['vote']
        identity = serializer.data['identity']

        ticket.known_approvers.remove(user)
        ticket.unknown_approvers.remove(user)
        ticket.known_denials.remove(user)
        ticket.unknown_denials.remove(user)

        if request_type == 1:   # set
            if vote == 1:   # approve
                if identity == 1:   # known
                    ticket.known_approvers.add(user)
                else:   # unknow
                    ticket.unknown_approvers.add(user)
            else:   # denial
                if identity == 1:   # known
                    ticket.known_denials.add(user)
                else:   # unknow
                    ticket.unknown_denials.add(user)
        else:   # unset
            pass

class ChangeStatusView(generics.UpdateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'

    queryset = Ticket.objects.all()
    serializer_class = ChangeStatusSerializer
    #TODO: set status permissions

class EditResponsiblesView(generics.CreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'

    queryset = Ticket.objects.all()
    serializer_class = EditResponsiblesSerializer

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        serializer.save(ticket=ticket)

class EditContributersView(generics.CreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'

    queryset = Ticket.objects.all()
    serializer_class = EditContributersSerializer

    def perform_create(self, serializer):
        ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        serializer.save(ticket=ticket)
