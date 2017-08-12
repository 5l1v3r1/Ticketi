from rest_framework import serializers
from models import Ticket

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
            'unknown_approvers',
            'known_denials',
            'unknown_denials',
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
