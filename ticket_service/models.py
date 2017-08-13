# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group, Permissoin
import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = CASCADE)
    post = models.CharField(max_length = 100)
    profile_picture_path = models.CharField(max_length = 500)


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
    adressed_users = models.ManyToManyField(User, related_name='ticket_M2M_adressed_users') #TODO: mitone khali bashe?
    cc_users = models.ManyToManyField(User, related_name='ticket_M2M_cc_users', blank=True)

    contributers = models.ManyToManyField(User, related_name='ticket_M2M_contributers')
    in_list_contributers = models.ManyToManyField(User, related_name='ticket_M2M_in_list_contributers', blank=True)

    is_public = models.BooleanField(default=True)
    being_unknown = models.BooleanField(default=False)
    tag_list = models.ManyToManyField('Tag', blank=True)
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

    status = models.CharField(choices = STATUS_CHOICES, default = PENDING, max_length = 15)

    need_to_confirmed = models.BooleanField(default = False)
    minimum_approvers_count = models.IntegerField(default = 0)

    parent = models.ForeignKey('Ticket', null = True, blank = True)

class PrivateTicket (models.Model):
    body = models.TextField()
    adressed_users = models.ManyToManyField(User)
    parent_ticket = models.ForeignKey('Ticket')

class Type (models.Model):
    title = models.CharField(max_length = 300)
    department = models.ManyToManyField('Department')

    def __str__(self):
        return self.title

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
    body = models.TextField()
    user = models.ForeignKey(User)
    ticket = models.ForeignKey('Ticket')
    creation_time = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('Comments', default = None)
    being_unknown = models.BooleanField(default = False)
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
