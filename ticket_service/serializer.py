from rest_framework import serializers
from models import Ticket
import datetime

class TicketSerializer(serializers.ModelSerializer):

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
#            'unknown_approvers',
            'known_denials',
#            'unknown_denials',
            'adressed_users',
            'cc_users',

            'in_list_contributers',
            'contributers',

            'is_public',
            'being_unknown',
            'tag_list',
            'creation_time',
            'status',

            'need_to_confirmed',
            'minimum_approvers_count',

            'parent',
        )
        read_only_fields = ('contributers', 'known_approvers', 'known_denials', 'creation_time', 'status', 'need_to_confirmed', 'minimum_approvers_count')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        ticket = Ticket(
            title = validated_data['title'],
            body = validated_data['body'],
            summary_len = validated_data['summary_len'],
            ticket_type = validated_data['ticket_type'],
            priority = validated_data['priority'],

            known_approvers = self.context['request'].user if validated_data['being_unknown'] else None,
            unknown_approvers = None if validated_data['being_unknown'] else self.context['request'].user,
            contributers = self.context['request'].user,
            being_unknown = validated_data['being_unknown'],

            creation_time = datetime.datetime.now(),
            status = Ticket.PENDING,

            adressed_users = validated_data['adressed_users'],
            cc_users = validated_data['cc_users'],
            in_list_contributers = validated_data['in_list_contributers'],

            is_public = validated_data['is_public'],
            tag_list = validated_data['tag_list'],
            parent = validated_data['parent'],
        )
        ticket.save()
        return ticket
