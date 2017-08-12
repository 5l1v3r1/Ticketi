# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime


class Ticket (models.Model):
    title = models.CharField(max_length = 500)
    body = models.TextField()
    summary_len = models.IntegerField()  #TODO : ye fkri b halesh bokonim -__-
    ticket_type = models.ForeignKey('Type')

    LOW = 'LOW'
    NORMAL = 'NORMAL'
    IMPORTANT = 'IMPORTANT'
    PRIORITY_CHOICES = (
        (LOW, "Low"),
        (NORMAL, "Normal"),
        (IMPORTANT, "Important"),
    )

    priority = models.CharField(choices = PRIORITY_CHOICES, default=NORMAL, max_length=15)
    known_approvers = models.ManyToManyField(User, related_name='ticket_M2M_known_approvers')
    unknown_approvers = models.ManyToManyField(User, related_name='ticket_M2M_unknown_approvers')
    known_denials = models.ManyToManyField(User, related_name='ticket_M2M_known_denials')
    unknown_denials = models.ManyToManyField(User, related_name='ticket_M2M_unknown_denials')
    adressed_users = models.ManyToManyField(User, related_name='ticket_M2M_adressed_users')
    cc_users = models.ManyToManyField(User, related_name='ticket_M2M_cc_users')

    in_list_contributers = models.ManyToManyField(User, related_name='ticket_M2M_in_list_contributers')
    contributers = models.ManyToManyField(User, related_name='ticket_M2M_contributers')

    is_public = models.BooleanField()
    being_unknown = models.BooleanField()
    tag_list = models.ManyToManyField('Tag')
    creation_time = models.DateField(auto_now_add=True)

    PENDING = 'PENDING'
    PROGRESSING = 'PROGRESSING'
    SOLVED = 'SOLVED'
    CLOSED = 'CLOSED'
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (PROGRESSING, "Progressing"),
        (SOLVED, "Solved"),
        (CLOSED, "Closed"),
    )

    status = models.CharField(choices = STATUS_CHOICES, default=PENDING, max_length=15)

    need_to_confirmed = models.BooleanField()
    minimum_approvers_count = models.IntegerField(default = 0)

    parent = models.ForeignKey('Ticket')

class PrivateTicket (models.Model):
    body = models.TextField()
    adressed_users = models.ManyToManyField(User)
    parent_ticket = models.ForeignKey('Ticket')

class Type (models.Model):
    title = models.CharField(max_length = 300)
    department = models.ManyToManyField('Department')

class Tag (models.Model):
    title = models.CharField(max_length = 100)

class Department (models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey('Department')
    level = models.IntegerField()

class Attachments (models.Model):
    path = models.CharField(max_length=500)

class PublicAttachments (Attachments):
    ticket = models.ForeignKey('Ticket')

class PrivateAttachments (Attachments):
    ticket = models.ForeignKey('PrivateTicket')

class Comments (models.Model):
    user = models.ForeignKey(User)
    ticket = models.ForeignKey('Ticket')
    creation_time = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('Comments')
    being_unknown = models.BooleanField()
    verified = models.BooleanField(default = False)

class Like (models.Model):
    comments = models.ForeignKey('Comments')
    user = models.ForeignKey(User)
    time = models.DateField(auto_now_add=True)

class Activities (models.Model):
    ticket = models.ForeignKey('Ticket')
    user = models.ForeignKey(User)
    time = models.DateField(auto_now_add=True)

class Referral (Activities):
    reffered_to = models.ManyToManyField(User)

class SetConfirmationLimit (Activities):
    limit_value = models.IntegerField(default = 0)
    need_to_confirmed = models.BooleanField(default = False)

class edit (Activities):
    new_body = models.TextField()
    new_title = models.CharField(max_length=500)

class ChangeStatus (Activities):
    status = models.CharField(choices = Ticket.STATUS_CHOICES, max_length=15)

class Reopen (Activities):
    new_ticket = models.ForeignKey('Ticket')
