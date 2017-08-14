from models import BaseActivity, Referral, SetConfirmationLimit, EditTicket, ChangeStatus, Reopen
# from ticket_service.serializer import UserSerializer
from rest_framework import serializers

class BaseActivitySerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=True)
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
        fields = BaseActivitySerializer.Meta.fields + ('new_title', 'new_body',)

class ReopenSerializer(BaseActivitySerializer):
    class Meta(BaseActivitySerializer.Meta):
        model = Reopen
        fields = BaseActivitySerializer.Meta.fields + ('new_ticket',)
