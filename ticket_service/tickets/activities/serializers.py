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
