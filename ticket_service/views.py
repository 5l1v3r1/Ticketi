# -*- coding: utf-8 -*-

from rest_framework import generics
from .serializer import TicketSerializer, CommentSerializer, TicketDetailsSerializer, LikeSerializer
from .models import Ticket, Comment, Like
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

    def perform_create(self, serializer):
        serializer.save()

class TicketDetailsView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketDetailsSerializer
    # permission_classes = [IsOwnerOrReadOnly]

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
