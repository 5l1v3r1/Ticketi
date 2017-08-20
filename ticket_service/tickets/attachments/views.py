from rest_framework import generics
from .models import (
    PrivateAttachment,
    PublicAttachment,
)
from .serializers import (
    PrivateAttachmentSerializer,
    PublicAttachmentSerializer
)

class PrivateAttachmentView(generics.ListCreateAPIView): #TODO: niazi nist
    queryset = PrivateAttachment.objects.all()
    serializer_class = PrivateAttachmentSerializer

class PublicAttachmentsView(generics.ListCreateAPIView): #TODO: b in niazi nist
    queryset = PublicAttachment.objects.all()
    serializer_class = PublicAttachmentSerializer

# class PrivateAttachmentsView(generics.ListCreateAPIView): #TODO: b in ham niazi nist
#     queryset = PrivateAttachment.objects.all()
#     serializer_class = PrivateAttachmentSerializer
