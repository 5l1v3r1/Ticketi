from rest_framework import generics
from .models import (
    Profile,
    ProfilePic,
)
from .serializers import (
    ProfilePicUploadSerializer,
    PublicProfileSerializer,
)
from rest_framework.permissions import (
    # IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)

class ProfilePicUploadView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProfilePic.objects.all()
    serializer_class = ProfilePicUploadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PublicProfileView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = PublicProfileSerializer
