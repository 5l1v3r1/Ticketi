from rest_framework import serializers
from .models import (
    Comment,
    Like,
)

class CommentSerializer(serializers.ModelSerializer):
    likes_nums = serializers.ReadOnlyField(source = 'likes_num') #TODO: (sadegh) man _count gozashtim, ye shekl konim, ya hame _num ya hame _count id:0
    user = serializers.SerializerMethodField()
    def get_user(self, comment):
        if not comment.being_unknown:
            serializer = UserSerializer(instance=comment.user)
            return serializer.data
        return None
    # body = serializers.SerializerMethodField() #TODO: baraye delete shode ha body eshoon ro khali bargardonim + ino uncomment konim toye new coooment moshkel mikhorim!
    # def get_body(self, comment):
    #     if not comment.deleted:
    #         return comment.body#TODO: verify 'parent' exist in that 'ticket'
    #     else:
    #         return ''

    class Meta:
        model = Comment
        fields = (
            'parent', 'ticket', 'body', 'id', 'user', 'creation_time', 'being_unknown', 'verified', 'likes_nums', 'edited',
        )
        read_only_fields = ('verified', 'user', 'edited' )

    def create(self, validated_data):
        comment = Comment(
            user = self.context['request'].user,
            body = validated_data['body'],
            being_unknown = validated_data['being_unknown'],
            creation_time = datetime.datetime.now(),
            parent = validated_data['parent'],
            ticket = validated_data['ticket'],
            verified = not validated_data['being_unknown'],
        )
        comment.save()
        return comment

class CommentDetailsSerializer(serializers.ModelSerializer):
    likes_nums = serializers.ReadOnlyField(source = 'likes_num') #TODO: (sadegh) man _count gozashtim, ye shekl konim, ya hame _num ya hame _count id:0
    user = serializers.SerializerMethodField()
    def get_user(self, comment):
        if not comment.being_unknown:
            serializer = UserSerializer(instance=comment.user)
            return serializer.data
        return None

    class Meta:
        model = Comment
        fields = (
            'body',
            'being_unknown',
            'parent',
            'ticket',
            'id',
            'user',
            'creation_time',
            'verified',
            'likes_nums',
            'edited',
            'deleted'
        )
        read_only_fields = (
            # 'body',
            # 'being_unknown',
            'parent',
            'ticket',
            'id',
            'user',
            'creation_time',
            'verified',
            'likes_nums',
            'edited',
            'deleted'
        )
    read_only_fields = ('deleted', )

    def update(self, instance, validated_data):
        new_body = validated_data['body']
        being_unknown = validated_data['being_unknown']

        if new_body != instance.body:
            instance.edited = True
            instance.body = new_body

        instance.being_unknown = being_unknown
        instance.verified = not being_unknown

        instance.save()
        return instance

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'comment')
        read_only_fields = ('id', 'user', 'comment')

class CommentJudgmentSerializer(serializers.ModelSerializer):
    REQUEST_TYPE_CHOICES = (
        (0, 'reject'),
        (1, 'accept')
    )
    request_type = serializers.ChoiceField(choices=REQUEST_TYPE_CHOICES)
    class Meta:
        model = Comment
        fields = ('request_type', )
