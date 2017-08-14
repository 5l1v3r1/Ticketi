from rest_framework import serializers
from models import Ticket, Type, Tag, Comment, BaseActivity, Like, PrivateAttachment, PublicAttachment
from models import Referral, SetConfirmationLimit, EditTicket, ChangeStatus, Reopen
from django.contrib.auth.models import User
import datetime
from django.db.models import Q


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
            'contributers', # read_only
            'need_to_confirmed', # read_only
            'minimum_approvers_count', # read_only
            'parent',
        )
        read_only_fields = ('creation_time', 'contributers', 'status', 'need_to_confirmed', 'minimum_approvers_count')
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

class CommentSerializer(serializers.ModelSerializer): #TODO: verify 'parent' exist in that 'ticket'
    likes_nums = serializers.ReadOnlyField(source = 'likes_count') #TODO: (sadegh) man _count gozashtim, ye shekl konim, ya hame _num ya hame _count id:0
    user = UserSerializer(read_only = True)
    class Meta:
        model = Comment
        fields = (
            'parent', 'ticket', 'body', 'id', 'user', 'creation_time', 'being_unknown', 'verified', 'likes_nums',
        )
        read_only_fields = ('verified', )


################################# Activities ###################################
class BaseActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Referral
        fields = ('id', 'user', 'time',)

class ReferralSerializer(serializers.ModelSerializer):
     class Meta(BaseActivitySerializer.Meta):
        model = Referral
        fields = BaseActivitySerializer.Meta.fields + ('reffered_to', )

class SetConfirmationLimitSerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = SetConfirmationLimit
        fields = BaseActivitySerializer.Meta.fields + ('limit_value', 'need_to_confirmed',)

class EditTicketSerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = EditTicket
        fields = BaseActivitySerializer.Meta.fields + ('new_title', 'new_body',)

class ChangeStatusSerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = ChangeStatus
        fields = BaseActivitySerializer.Meta.fields + ('status',)

class ReopenSerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = Reopen
        fields = BaseActivitySerializer.Meta.fields + ('new_ticket',)
################################################################################


class TicketDetailsSerializer(serializers.ModelSerializer):
    known_approvers = UserSerializer(many=True, read_only=True)
    known_denials = UserSerializer(many=True, read_only=True)
    ticket_type = TypeSerializer(read_only=True) #TODO: baraye write bayad avaz beshe
    approvers_count = serializers.ReadOnlyField(source='get_approvers_count')
    denials_count = serializers.ReadOnlyField(source='get_denials_count')
    addressed_users = UserSerializer(many=True, read_only=True) #TODO: test konim ke in kar mikone asan ya na!
    cc_users = UserSerializer(many=True, read_only=True) #TODO: test konim ke in kar mikone asan ya na!
    tag_list = TagSerializer(many=True, read_only=True)

    comments = serializers.SerializerMethodField('get_comments2') #TODO: edit name
    contributers = serializers.SerializerMethodField('get_contributers2')   #TODO: edit name
    in_list_contributers = serializers.SerializerMethodField('get_in_list_contributers2')   #TODO: edit name
    activities = serializers.SerializerMethodField('get_activities2')   #TODO: edit name

    def get_activities2(self, ticket):
        referral = ReferralSerializer(instance=Referral.objects.filter(Q(ticket=ticket)), many=True)
        setConfirmationLimit = SetConfirmationLimitSerializer(instance=SetConfirmationLimit.objects.filter(Q(ticket=ticket)), many=True)
        editTicket = EditTicketSerializer(instance=EditTicket.objects.filter(Q(ticket=ticket)), many=True)
        changeStatus = ChangeStatusSerializer(instance=ChangeStatus.objects.filter(Q(ticket=ticket)), many=True)
        reopen = ReopenSerializer(instance=Reopen.objects.filter(Q(ticket=ticket)), many=True)
        return {
            'referral': referral.data,
            'setConfirmationLimit': setConfirmationLimit.data,
            'editTicket': editTicket.data,
            'changeStatus': changeStatus.data,
            'reopen': reopen.data
        }


    def get_comments2(self, ticket):
        queryset = []
        requested_user = self.context['request'].user
        if requested_user in ticket.contributers.all():
            queryset = Comment.objects.filter(Q(ticket=ticket))
        else:
            queryset = Comment.objects.filter(Q(ticket=ticket) & Q(verified=True))

        serializer = CommentSerializer(instance=queryset, many=True)
        return serializer.data

    def get_contributers2(self, ticket):
        queryset = []
        requested_user = self.context['request'].user
        if not ticket.being_unknown or \
        requested_user in ticket.contributers.all() or \
        requested_user in ticket.in_list_contributers.all():
            queryset = ticket.contributers.all()

        serializer = UserSerializer(instance=queryset, many=True)
        return serializer.data

    def get_in_list_contributers2(self, ticket):
        queryset = []
        requested_user = self.context['request'].user
        if requested_user in ticket.contributers.all() or \
        requested_user in ticket.in_list_contributers.all():
            queryset = ticket.in_list_contributers.all()

        serializer = UserSerializer(instance=queryset, many=True)
        return serializer.data

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
            'addressed_users',
            'cc_users',
            'contributers',
            'in_list_contributers',
            'is_public',
            'being_unknown',
            'tag_list',
            'creation_time',
            'status',
            'need_to_confirmed',
            'minimum_approvers_count',
            'parent',
            'activities',
            'comments',
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

class PublicAttachmentSerializer(BaseAttachmentSerializer):
    class Meta(BaseAttachmentSerializer.Meta):
        model = PublicAttachment
        fields = BaseAttachmentSerializer.Meta.fields + ('ticket', )

class PrivateAttachmentSerializer(BaseAttachmentSerializer):
    class Meta(BaseAttachmentSerializer.Meta):
        model = PrivateAttachment
        fields = BaseAttachmentSerializer.Meta.fields + ('ticket', )
