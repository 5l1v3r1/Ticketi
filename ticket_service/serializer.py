from rest_framework import serializers
from models import (
    Ticket,
    Type,
    Tag,
    Comment,
    BaseActivity,
    Like,
    PrivateAttachment,
    PublicAttachment,
    BaseAttachment,
)
from models import (
    ReferralActiviy,
    SetConfirmationLimitActiviy,
    EditTicketActivity,
    ChangeStatusActivity,
    ReopenActivity,
    ProfilePic,
    Profile,
    PrivateTicket,
)
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
import json

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title', )

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'title')

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

# class PersonalProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     picture_path = serializers.SerializerMethodField()

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

class PrivateTicketSerializer(serializers.ModelSerializer):
    addressed_users = UserSerializer(many=True)
    # parent_ticket = TicketSerializer(read_only=True)
    private_attachment = PrivateAttachmentSerializer(many=True)

    class Meta:
        model = PrivateTicket
        fields = ('body', 'addressed_users', 'parent_ticket', 'private_attachment')

class TicketSerializer(serializers.ModelSerializer):
    contributers = UserSerializer(many=True, read_only=True, source='get_contributers')
    # ticket_type = TypeSerializer() #TODO: baraye write bayad avaz beshe
    summary = serializers.ReadOnlyField(source='get_summary_body')
    approvers_count = serializers.ReadOnlyField(source='get_approvers_count')
    denials_count = serializers.ReadOnlyField(source='get_denials_count')
    addressed_users = UserSerializer(many=True) #TODO: test konim ke in kar mikone asan ya na!
    cc_users = UserSerializer(many=True) #TODO: test konim ke in kar mikone asan ya na!
    tag_list = TagSerializer(many=True)
    public_attachments = PublicAttachmentSerializer(many=True, source="get_public_attachments")
    private_ticket = PrivateTicketSerializer(many=True, source='get_private_ticket')

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
            'public_attachments',
            'private_ticket',
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

        # ticket.public_attachments.add(PublicAttachmentSerializer.save(parent_ticket=ticket))

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
    #         return comment.body
    #     else:
    #         return ''

    class Meta:                                       #DONE: ejazeye delete ba permission dade beshe
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

################################# Activities ###################################
class BaseActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ReferralActiviy
        fields = ('id', 'user', 'time',)

class ReferralActivitySerializer(serializers.ModelSerializer):
     class Meta(BaseActivitySerializer.Meta):
        model = ReferralActiviy
        fields = BaseActivitySerializer.Meta.fields + ('reffered_to', )

class SetConfirmationLimitActivitySerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = SetConfirmationLimitActiviy
        fields = BaseActivitySerializer.Meta.fields + ('limit_value', 'need_to_confirmed',)

class EditTicketActivitySerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = EditTicketActivity
        fields = BaseActivitySerializer.Meta.fields + ('prev_title', 'prev_body',)

class ChangeStatusActivitySerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = ChangeStatusActivity
        fields = BaseActivitySerializer.Meta.fields + ('status',)

class ReopenActivitySerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = ReopenActivity
        fields = BaseActivitySerializer.Meta.fields + ('new_ticket',)
################################################################################


class TicketDetailsSerializer(serializers.ModelSerializer): #TODO: ye field hayi ham bayad ezafe beshe vase inke masalan ray ma chi bode o ina!
    known_approvers = UserSerializer(many=True, read_only=True)
    known_denials = UserSerializer(many=True, read_only=True)
    ticket_type = TypeSerializer(read_only=True) #TODO: baraye write bayad avaz beshe
    approvers_count = serializers.ReadOnlyField(source='get_approvers_count')
    denials_count = serializers.ReadOnlyField(source='get_denials_count')
    addressed_users = UserSerializer(many=True, read_only=True) #TODO: test konim ke in kar mikone asan ya na!
    cc_users = UserSerializer(many=True, read_only=True) #TODO: test konim ke in kar mikone asan ya na!
    tag_list = TagSerializer(many=True, read_only=True)

    comments = serializers.SerializerMethodField() #DONE: edit name
    contributers = serializers.SerializerMethodField()   #DONE: edit name
    in_list_contributers = serializers.SerializerMethodField()   #DONE: edit name
    activities = serializers.SerializerMethodField()   #DONE: edit name

    def get_activities(self, ticket):
        referral = ReferralActivitySerializer(instance=ReferralActiviy.objects.filter(Q(ticket=ticket)), many=True)
        setConfirmationLimit = SetConfirmationLimitActivitySerializer(instance=SetConfirmationLimitActiviy.objects.filter(Q(ticket=ticket)), many=True)
        editTicket = EditTicketActivitySerializer(instance=EditTicketActivity.objects.filter(Q(ticket=ticket)), many=True)
        changeStatus = ChangeStatusActivitySerializer(instance=ChangeStatusActivity.objects.filter(Q(ticket=ticket)), many=True)
        reopen = ReopenActivitySerializer(instance=ReopenActivity.objects.filter(Q(ticket=ticket)), many=True)
        return {
            'referral': referral.data,
            'setConfirmationLimit': setConfirmationLimit.data,
            'editTicket': editTicket.data,
            'changeStatus': changeStatus.data,
            'reopen': reopen.data
        }


    def get_comments(self, ticket):
        queryset = []
        requested_user = self.context['request'].user
        if requested_user in ticket.contributers.all():
            queryset = Comment.objects.filter(Q(ticket=ticket) & Q(deleted=False))
        else:
            queryset = Comment.objects.filter(Q(ticket=ticket) & Q(verified=True) & Q(deleted=False))

        serializer = CommentSerializer(instance=queryset, many=True)
        return serializer.data

    def get_contributers(self, ticket):
        queryset = []
        requested_user = self.context['request'].user
        if not ticket.being_unknown or \
        requested_user in ticket.contributers.all() or \
        requested_user in ticket.in_list_contributers.all():
            queryset = ticket.contributers.all()

        serializer = UserSerializer(instance=queryset, many=True)
        return serializer.data

    def get_in_list_contributers(self, ticket):
        queryset = []
        requested_user = self.context['request'].user
        if requested_user in ticket.contributers.all() or \
        requested_user in ticket.in_list_contributers.all():
            queryset = ticket.in_list_contributers.all()

        serializer = UserSerializer(instance=queryset, many=True)
        return serializer.data

    # def update(self, instance, validated_data):
    #     pass

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
            'public_attachments',
        )
        read_only_fields = (
            'id',
            # 'title',
            # 'body',
            # 'summary_len',
            # 'ticket_type',
            # 'priority',
            'known_approvers',
            'known_denials',
            'approvers_count',
            'denials_count',
            'addressed_users',
            'cc_users',
            'contributers',
            'in_list_contributers', #TODO: edit in ham bayad ezafe beshe!
            'is_public',
            # 'being_unknown',
            # 'tag_list',
            'creation_time',
            'status',
            'need_to_confirmed',
            'minimum_approvers_count',
            'parent',
            'activities',
            'comments',
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

class ContributeSerializer(serializers.ModelSerializer):
    REQUEST_TYPE_CHOICES = (
        (0, 'reject'),
        (1, 'accept')
    )
    request_type = serializers.ChoiceField(choices=REQUEST_TYPE_CHOICES)
    class Meta:
        model = Ticket
        fields = ('request_type', )

class CommentJudgmentSerializer(serializers.ModelSerializer):
    REQUEST_TYPE_CHOICES = (
        (0, 'reject'),
        (1, 'accept')
    )
    request_type = serializers.ChoiceField(choices=REQUEST_TYPE_CHOICES)
    class Meta:
        model = Comment
        fields = ('request_type', )

class VoteSerializer(serializers.ModelSerializer):
    REQUEST_TYPE_CHOICES = (
        (0, 'unset'),
        (1, 'set')
    )

    VOTE_CHOICES = (
        (0, 'denial'),
        (1, 'approve')
    )

    IDENTITY_CHOICES = (
        (0, 'unknown'),
        (1, 'known')
    )

    request_type = serializers.ChoiceField(choices=REQUEST_TYPE_CHOICES)
    vote = serializers.ChoiceField(choices=VOTE_CHOICES)
    identity = serializers.ChoiceField(choices=IDENTITY_CHOICES)
    class Meta:
        model = Ticket
        fields = ('request_type', 'vote', 'identity', )

class SetNeedToConfirmedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('need_to_confirmed', 'minimum_approvers_count', )

class ChangeStatusSerializer(serializers.ModelSerializer):
    STATUS_CHOICES = (
        (0, 'open'),
        (1, 'waiting'),
        (2, 'inProgress'),
        (3, 'finished'),
        (4, 'closed'),
        (5, 'cancled'),
        (6, 'blocked'),
    )
    status = serializers.ChoiceField(choices=Ticket.STATUS_CHOICES)
    class Meta:
        model = Ticket
        fields = ('status', )

class EditResponsiblesSerializer(serializers.ModelSerializer):
    REQUEST_TYPE_CHOICES = (
        (0, 'add'),
        (1, 'delete')
    )
    ADD_AS_CHOICES = (
        (0, 'addressed'),
        (1, 'cc')
    )
    username = serializers.CharField(write_only=True)
    request_type = serializers.ChoiceField(choices=REQUEST_TYPE_CHOICES, write_only=True)
    add_as = serializers.ChoiceField(choices=ADD_AS_CHOICES, write_only=True)
    class Meta:
        model = Ticket
        fields = ('username', 'request_type', 'add_as', )

    def create(self, validated_data):
        ticket = validated_data['ticket']
        user = User.objects.get(username=validated_data['username'])

        if validated_data['request_type'] == 0: # add
            if validated_data['add_as'] == 0: # addressed_users
                ticket.cc_users.remove(user)
                ticket.addressed_users.add(user)
            else:   # cc_users
                ticket.addressed_users.remove(user)
                ticket.cc_users.add(user)
        else:   # remove
            ticket.addressed_users.remove(user)
            ticket.cc_users.remove(user)

        return ticket

class EditContributersSerializer(serializers.ModelSerializer):
    REQUEST_TYPE_CHOICES = (
        (0, 'add'),
        (1, 'delete')
    )
    ADD_AS_CHOICES = (
        (0, 'addressed'),
        (1, 'cc')
    )
    username = serializers.CharField(write_only=True)
    request_type = serializers.ChoiceField(choices=REQUEST_TYPE_CHOICES, write_only=True)
    class Meta:
        model = Ticket
        fields = ('username', 'request_type',)

    def create(self, validated_data):
        ticket = validated_data['ticket']
        user = User.objects.get(username=validated_data['username'])

        if validated_data['request_type'] == 0: # add
            if user not in ticket.contributers.all():
                ticket.in_list_contributers.add(user)
        else:   # remove
            ticket.in_list_contributers.remove(user)

        return ticket
