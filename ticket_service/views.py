# -*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from .serializer import (
    TicketSerializer,
    CommentSerializer,
    TicketDetailsSerializer,
    LikeSerializer,
    PrivateAttachmentSerializer,
    PublicAttachmentSerializer,
    ProfilePicUploadSerializer,
    PublicProfileSerializer,
    PrivateTicketSerializer,
)
from .models import (
    Ticket,
    Comment,
    Like,
    PrivateAttachment,
    PublicAttachment,
    Profile,
    ProfilePic,
    PrivateTicket,
)
from rest_framework.pagination import PageNumberPagination
from permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = StandardResultsSetPagination

    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     serializer.save(private_ticket=PrivateTicket(parent_ticket=instance))

class TicketDetailsView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailsSerializer

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class PrivateAttachmentView(generics.ListCreateAPIView): #TODO: niazi nist
    queryset = PrivateAttachment.objects.all()
    serializer_class = PrivateAttachmentSerializer

class PublicAttachmentsView(generics.ListCreateAPIView): #TODO: b in niazi nist
    queryset = PublicAttachment.objects.all()
    serializer_class = PublicAttachmentSerializer

class PrivateAttachmentsView(generics.ListCreateAPIView): #TODO: b in ham niazi nist
    queryset = PrivateAttachment.objects.all()
    serializer_class = PrivateAttachmentSerializer

class ProfilePicUploadView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfilePic.objects.all()
    serializer_class = ProfilePicUploadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PublicProfileView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = PublicProfileSerializer

class PrivateTicketView(generics.ListCreateAPIView): #TODO: be in aslan niazi nist, vase teste. (chon listo support nemikone -_-)
    queryset = PrivateTicket.objects.all()
    serializer_class = PrivateTicketSerializer
