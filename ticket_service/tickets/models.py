
from django.db import models
from django.contrib.auth.models import User

class Ticket (models.Model):
    title = models.CharField(max_length = 500)
    body = models.TextField()
    summary_len = models.IntegerField(default=0)  #TODO : ye fkri b halesh bokonim -__-
    ticket_type = models.ForeignKey('Type', blank = True, null = True) #TODO: nabayad beshe blank gozasht, movaqat intori shod

    LOW = 'LOW'
    NORMAL = 'NORMAL'
    IMPORTANT = 'IMPORTANT'
    PRIORITY_CHOICES = (
        (LOW, "Low"),
        (NORMAL, "Normal"),
        (IMPORTANT, "Important"),
    )

    priority = models.CharField(choices = PRIORITY_CHOICES, default=NORMAL, max_length=15)
    known_approvers = models.ManyToManyField(User, related_name='ticket_M2M_known_approvers', blank=True)
    unknown_approvers = models.ManyToManyField(User, related_name='ticket_M2M_unknown_approvers', blank=True)
    known_denials = models.ManyToManyField(User, related_name='ticket_M2M_known_denials', blank=True)
    unknown_denials = models.ManyToManyField(User, related_name='ticket_M2M_unknown_denials', blank=True)
    addressed_users = models.ManyToManyField(User, related_name='addressed_users', blank=True) #TODO: mitone khali bashe? #TODO: remove (blank=True) for production + baraye edit draft bayad beshe faghat
    cc_users = models.ManyToManyField(User, related_name='ticket_M2M_cc_users', blank=True)

    contributers = models.ManyToManyField(User, related_name='ticket_M2M_contributers')
    in_list_contributers = models.ManyToManyField(User, related_name='ticket_M2M_in_list_contributers', blank=True)

    is_public = models.BooleanField(default=True)
    being_unknown = models.BooleanField(default=False)
    tag_list = models.ManyToManyField('Tag', blank=True)
    creation_time = models.DateField(auto_now_add=True) #TODO: ezafe kardane saAt
    is_draft = models.BooleanField(default=True)

    OPEN = 'OPEN'
    WAITING = 'WAITING'
    INPROGRESS = 'INPROGRESS'
    FINISHED = 'FINISHED'
    BLOCKED = 'BLOCKED'
    SOLVED = 'SOLVED'
    CANCLED = 'CANCLED'
    STATUS_CHOICES = (
        (OPEN, OPEN),
        (WAITING, WAITING),
        (INPROGRESS, INPROGRESS),
        (FINISHED, FINISHED),
        (BLOCKED, BLOCKED),
        (SOLVED, SOLVED),
        (CANCLED, CANCLED),
    )

    status = models.CharField(choices = STATUS_CHOICES, default = OPEN, max_length = 15)

    need_to_confirmed = models.BooleanField(default = False)
    minimum_approvers_count = models.IntegerField(default = 0)

    parent = models.ForeignKey('Ticket', null = True, blank = True)
    # def update(self, *args, **kwargs):
    #     pass

    @property
    def get_summary_body(self):
        return self.body[0:self.summary_len]

    @property
    def get_approvers_count(self):
        return self.known_approvers.count() + self.unknown_approvers.count()

    @property
    def get_denials_count(self):
        return self.known_denials.count() + self.unknown_denials.count()

    @property
    def get_public_attachments(self):
        return self.publicattachment_set.all()

    @property
    def get_private_ticket(self):
        return self.privateticket_set.all()

    def __str__(self):
        return self.title

class PrivateTicket (models.Model):
    parent_ticket = models.ForeignKey('Ticket')
    body = models.TextField()
    addressed_users = models.ManyToManyField(User)

    @property
    def get_private_attachments(self):
        return self.privateattachment_set.all()

class Type (models.Model):
    title = models.CharField(max_length = 300)
    department = models.ManyToManyField('Department')

    def __str__(self):
        return self.title

class Tag (models.Model):
    title = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

class Department (models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('Department')
    level = models.IntegerField()

    def __str__(self):
        return self.title

from .activities import models
from .attachments import models
from .comments import models
