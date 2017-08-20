from rest_framework import serializers
import json
from .models import (
    BaseAttachment,
    PublicAttachment,
    PrivateAttachment
)

class BaseAttachmentSerializer(serializers.ModelSerializer):
    pic = json.dumps(unicode('pic'))
    class Meta:
        model = BaseAttachment
        fields = ('pic', 'description', )

class PublicAttachmentSerializer(BaseAttachmentSerializer):
    class Meta(BaseAttachmentSerializer.Meta):
        model = PublicAttachment
        fields = BaseAttachmentSerializer.Meta.fields + ('ticket', )

class PrivateAttachmentSerializer(BaseAttachmentSerializer):
    class Meta(BaseAttachmentSerializer.Meta):
        model = PrivateAttachment
        fields = BaseAttachmentSerializer.Meta.fields + ('ticket', )
