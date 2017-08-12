# -*- coding: utf-8 -*-

from rest_framework import generics
from .serializer import TicketSerializer
from .models import Ticket

class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        serializer.save()
