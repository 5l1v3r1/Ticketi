# -*- coding: utf-8 -*-

from rest_framework import generics
from .serializer import TicketSerializer
from .models import Ticket
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
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrReadOnly]
