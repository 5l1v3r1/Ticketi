# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime


class Ticket (models.Model):
    title = models.CharField(max_length = 500)
    body = models.TextField()
    summary_len = models.IntegerField()  #TODO : ye fkri b halesh bokonim -__-
    type_ = models.ForeignKey(Type)

    PRIORITY_CHOICES = (
        (1, "Low"),
        (2, "Normal"),
        (3, "Important"),
    )

    priority = ChoiceField(CHOICES = PRIORITY_CHOICES)

    known_approvers = models.ManyToManyField(User)
    unknown_approvers = models.ManyToManyField(User)
    known_denials = models.ManyToManyField(User)
    unknown_denials = models.ManyToManyField(User)
    adressed_users = models.ManyToManyField(User)
    cc_users = models.ManyToManyField(User)

    in_list_contributers = models.ManyToManyField(User)
    contributers = models.ManyToManyField(User)

    is_public = models.BooleanField()
    being_unknown = models.BooleanField()
    tag_list = models.ManyToManyField(Tag)
    creation_time = DateField(default = datetime.now())

    STATUS_CHOICES = (
        (1, "Pending"),
        (2, "Progressing"),
        (3, "Solved"),
        (4, "Closed"),
    )

    status = ChoiceField(CHOICES = STATUS_CHOICES)

    need_to_confirmed = models.BooleanField()
    minimum_approvers_count = models.IntegerField(default = 0)

    parent = models.ForeignKey(Ticket)

class PrivateTicket (models.Model):
    body = models.TextField()
    adressed_users = models.ManyToManyField(User)
    parent_ticket = models.ForeignKey(Ticket)

class Type (models.Model):
    title = models.CharField(max_length = 300)
    department = models.ManyToManyField(Department)

class Tag (models.Model):
    title = models.CharField(max_length = 100)

class Department (models.Model):
    title = models.CharField()
    parent = models.ForeignKey(Department)
    level = IntegerField()

class Attachments (models.Model):
    path = models.CharField()

class PublicAttachments (Attachments):
    ticket = models.ForeignKey(Ticket)

class PrivateAttachments (Attachments):
    ticket = models.ForeignKey(PrivateTicket)

class Comments (models.Model):
    user = models.ForeignKey(User)
    ticket = models.ForeignKey(Ticket)
    creation_time = models.DateField(default = datetime.now())
    parent = models.ForeignKey(Comments)
    being_unknown = models.BooleanField()
    verified = models.BooleanField(default = False)

class Like (models.Model):
    comments = models.ForeignKey(Comments)
    user = models.ForeignKey(User)
    time = models.DateField(default = datetime.now())

class Activities (model.Model):
    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(User)
    time = models.DateField(default = datetime.now())

class Referral (Activities):
    reffered_to = models.ManyToManyField(User)

class SetConfirmationLimit (Activities):
    limit_value = models.IntegerField(default = 0)
    need_to_confirmed = models.BooleanField(default = False)

class edit (Activities):
    new_body = models.TextField()
    new_title = models.CharField()

class ChangeStatus (Activities):
    status = ChoiceField(Ticket.STATUS_CHOICES)

class Reopen (Activities):
    new_ticket = models.ForeignKey(Ticket)
