from django.db import models
from django.contrib.auth.models import User
from ticket_service.tickets.models import *

class BaseActivity (models.Model):
    ticket = models.ForeignKey('Ticket', related_name="%(app_label)s_%(class)s_related",
                                related_query_name="%(app_label)s_%(class)s_relateds",)
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related",
                                related_query_name="%(app_label)s_%(class)s_relateds",)
    time = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class ReferralActiviy (BaseActivity):
    reffered_to = models.ManyToManyField(User)

class SetConfirmationLimitActiviy (BaseActivity):
    limit_value = models.IntegerField(default = 0)
    need_to_confirmed = models.BooleanField(default = False)

class EditTicketActivity (BaseActivity):
    prev_title = models.CharField(max_length=500)
    prev_body = models.TextField()

class ChangeStatusActivity (BaseActivity):
    status = models.CharField(choices = Ticket.STATUS_CHOICES, max_length=15)

class ReopenActivity (BaseActivity):
    new_ticket = models.ForeignKey('Ticket')
