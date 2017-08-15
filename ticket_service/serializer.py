from rest_framework import serializers
from models import Ticket, Type, Tag, Comment, BaseActivity, Like
from django.contrib.auth.models import User
import datetime

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseActivity
        fields = ('id', )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title', )

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'title')

class UserSerializer(serializers.ModelSerializer):
    picture_path = serializers.ReadOnlyField(source='profile.picture_path')
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'picture_path')

class TicketSerializer(serializers.ModelSerializer):
    contributers = UserSerializer(many=True, read_only=True, source='get_contributers')
    # ticket_type = TypeSerializer() #TODO: baraye write bayad avaz beshe
    summary = serializers.ReadOnlyField(source='get_summary_body')
    approvers_count = serializers.ReadOnlyField(source='get_approvers_count')
    denials_count = serializers.ReadOnlyField(source='get_denials_count')
    addressed_users = UserSerializer(many=True) #TODO: test konim ke in kar mikone asan ya na!
    cc_users = UserSerializer(many=True) #TODO: test konim ke in kar mikone asan ya na!
    tag_list = TagSerializer(many=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'title',
            'body', # write_only
            'summary_len', # write_only
            'in_list_contributers', # write_only
            'summary',
            'ticket_type',
            'priority',
            'approvers_count',
            'denials_count',
            'addressed_users',
            'cc_users',
            'is_public',
            'being_unknown',
            'tag_list',
            'creation_time', # read_only
            'status', # read_only
            'contributers',
            'need_to_confirmed', # read_only
            'minimum_approvers_count', # read_only
            'parent',
        )
        read_only_fields = ('creation_time', 'status', 'need_to_confirmed', 'minimum_approvers_count')
        extra_kwargs = {
            'body': {'write_only': True},
            'summary_len': {'write_only': True},
            'in_list_contributers': {'write_only': True}
        }

    def create(self, validated_data):
        ticket = Ticket(
            title = validated_data['title'],
            body = validated_data['body'],
            summary_len = validated_data['summary_len'],
            ticket_type = validated_data['ticket_type'],
            priority = validated_data['priority'],
            being_unknown = validated_data['being_unknown'],
            creation_time = datetime.datetime.now(),
            status = Ticket.PENDING,
            is_public = validated_data['is_public'],
            parent = validated_data['parent'],
        )
        ticket.save()

        # TODO: khode user ro az list 'in_list_contributers' o 'addressed_users' o 'cc_users' ina hazf konim!
        ticket.contributers.add(self.context['request'].user)
        map(lambda user: ticket.addressed_users.add(user), validated_data['addressed_users'])
        map(lambda user: ticket.cc_users.add(user), validated_data['cc_users'])
        map(lambda user: ticket.in_list_contributers.add(user), validated_data['in_list_contributers'])
        map(lambda tag: ticket.tag_list.add(tag), validated_data['tag_list'])

        if not validated_data['being_unknown']:
            ticket.known_approvers.add(self.context['request'].user)
        else:
            ticket.unknown_approvers.add(self.context['request'].user)

        return ticket

class CommentSerializer(serializers.ModelSerializer):
    likes_nums = serializers.ReadOnlyField(source = 'likes_count')
    user = UserSerializer(read_only = True)
    class Meta:
        model = Comment
        fields = (
            'parent', 'ticket', 'body', 'id', 'user', 'creation_time', 'being_unknown', 'verified', 'likes_nums',
        )
        read_only_fields = ('verified', )

class TicketDetailsSerializer(serializers.ModelSerializer):

    known_approvers = UserSerializer(many=True, read_only=True)
    known_denials = UserSerializer(many=True, read_only=True)
    ticket_type = TypeSerializer(read_only=True) #TODO: baraye write bayad avaz beshe
    approvers_count = serializers.ReadOnlyField(source='get_approvers_count')
    denials_count = serializers.ReadOnlyField(source='get_denials_count')
    addressed_users = UserSerializer(many=True, read_only=True) #TODO: test konim ke in kar mikone asan ya na!
    cc_users = UserSerializer(many=True, read_only=True) #TODO: test konim ke in kar mikone asan ya na!
    contributers = UserSerializer(many=True, read_only=True, source='get_contributers')
    tag_list = TagSerializer(many=True, read_only=True)
    Comment = UserSerializer(many=True, read_only=True, source='get_contributers') #TODO: test comment
    Activity = ActivitySerializer(many=True, source='get_activities')

    class Meta:
        model = Ticket
        fields = (
            'id',
            'title',
            'body',
            'summary_len',
            'ticket_type',
            'priority',
            'known_approvers',
            'known_denials',
            'approvers_count',
            'denials_count',
            'Comment',
            'addressed_users',
            'cc_users',
            'contributers',
            'is_public',
            'being_unknown',
            'tag_list',
            'creation_time',
            'status',
            'need_to_confirmed',
            'minimum_approvers_count',
            'parent',
            'Activity'
        )

class LikeSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Like
        fields = (
            'id', 'user', 'time', 'Comment',
        )
class BaseAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseActivity
        fields = ('path', )
