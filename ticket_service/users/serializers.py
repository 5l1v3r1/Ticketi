from rest_framework import serializers
from django.contrib.auth.models import User
import json

from .models import (
    ProfilePic,
    Profile
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', )

class ProfilePicUploadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    pic = json.dumps(unicode('pic'))
    class Meta:
        model = ProfilePic
        fields = ('pic', 'user', )

class PublicProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    picture_path = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('user', 'post', 'picture_path', )

    def get_picture_path(self, profile):
        queryset = ProfilePic.objects.filter(Q(user=profile.user))
        serializer = ProfilePicUploadSerializer(instance=queryset, many=True)
        return serializer.data
