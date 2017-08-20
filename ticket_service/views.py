# -*- coding: utf-8 -*-

from rest_framework import generics
from .models import Ticket, Comment, Like, PrivateAttachment, PublicAttachment, SetConfirmationLimitActiviy, EditTicketActivity, ReopenActivity
from rest_framework.pagination import PageNumberPagination
from permissions import IsOwnerOrReadOnly, IsInListContributers
from django.db.models import Q

from .serializer import TicketSerializer, \
                        CommentSerializer, \
                        CommentDetailsSerializer, \
                        CommentJudgmentSerializer, \
                        TicketDetailsSerializer, \
                        PrivateAttachmentSerializer, \
                        PublicAttachmentSerializer, \
                        ContributeSerializer, \
                        LikeSerializer, \
                        VoteSerializer, \
                        SetNeedToConfirmedSerializer, \
                        ChangeStatusSerializer, \
                        EditResponsiblesSerializer, \
                        EditContributersSerializer

from rest_framework.views import APIView

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

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
    # permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        EditTicketActivity(
            user = self.request.user,
            ticket = ticket,
            prev_title = ticket.title,
            prev_body = ticket.body
        ).save()
        serializer.save()


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailsView(generics.RetrieveUpdateDestroyAPIView):    #TODO: permission vase sahabesh va contributers
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
    serializer_class = CommentDetailsSerializer

    def perform_destroy(self, serializer):
        serializer.deleted = True
        serializer.save()
        return serializer

class CommentJudgmentView(generics.CreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id'
    queryset = Comment.objects.all()
    serializer_class = CommentJudgmentSerializer

    def perform_create(self, serializer):
        request_type = serializer.validated_data['request_type']
        comment = Comment.objects.get(id=self.kwargs['comment_id'])

        if request_type == 1: # accept
            comment.verified = True
        else: # reject
            comment.verified = False
            comment.deleted = True
        comment.save()

class LikeView(generics.CreateAPIView):
    lookup_field = 'comment_id'
    lookup_url_kwarg = 'comment_id'
    serializer_class = LikeSerializer

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        return Like.objects.filter(Q(comment_id = comment_id))

    def perform_create(self, serializer):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        user = self.request.user
        serializer.save(user=user, comment=comment)

class DislikeView(generics.DestroyAPIView):
    lookup_field = 'comment_id'
    lookup_url_kwarg = 'comment_id'
    serializer_class = LikeSerializer

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        user = self.request.user
        return Like.objects.filter(Q(comment_id=comment_id) & Q(user=user))

class PrivateAttachmentView(generics.ListCreateAPIView):
    queryset = PrivateAttachment.objects.all()
    serializer_class = PrivateAttachmentSerializer

class PublicAttachmentsView(generics.ListCreateAPIView):
    queryset = PublicAttachment.objects.all()
    serializer_class = PublicAttachmentSerializer

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
            need_to_confirmed = serializer.data['need_to_confirmed'],
            limit_value = serializer.data['minimum_approvers_count']
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
