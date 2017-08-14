# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import json

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    post = models.CharField(max_length = 100)
    picture_path = models.CharField(max_length = 500)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


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
    addressed_users = models.ManyToManyField(User, related_name='addressed_users') #TODO: mitone khali bashe?
    cc_users = models.ManyToManyField(User, related_name='ticket_M2M_cc_users', blank=True)

    contributers = models.ManyToManyField(User, related_name='ticket_M2M_contributers')
    in_list_contributers = models.ManyToManyField(User, related_name='ticket_M2M_in_list_contributers', blank=True)

    is_public = models.BooleanField(default=True)
    being_unknown = models.BooleanField(default=False)
    tag_list = models.ManyToManyField('Tag', blank=True)
    creation_time = models.DateField(auto_now_add=True) #TODO: ezafe kardane saAt

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

    @property
    def get_summary_body(self):
        return self.body[0:self.summary_len]

    @property
    def get_approvers_count(self):
        return self.known_approvers.count() + self.unknown_approvers.count()

    @property
    def get_denials_count(self):
        return self.known_denials.count() + self.unknown_denials.count()

    def __str__(self):
        return self.title

class PrivateTicket (models.Model):
    body = models.TextField()
    addressed_users = models.ManyToManyField(User)
    parent_ticket = models.ForeignKey('Ticket')

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

class BaseAttachment (models.Model): #DONE: esm az halate jam kharej beshe
    path = models.CharField(max_length=500)
    class Meta:
        abstract = True

class PublicAttachment (BaseAttachment): #DONE: esm az halate jam kharej beshe
    ticket = models.ForeignKey('Ticket')

class PrivateAttachment (BaseAttachment): #DONE: esm az halate jam kharej beshe
    ticket = models.ForeignKey('PrivateTicket')

class Comment (models.Model): #TODO: ye field ham bayad bezaarim ke age delete shod TRUE beshe #DONE: esm az halate jam kharej beshe
    body = models.TextField()
    user = models.ForeignKey(User)
    ticket = models.ForeignKey('Ticket')
    creation_time = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('Comment', default = None, null = True, blank = True)
    being_unknown = models.BooleanField(default = False)
    verified = models.BooleanField(default = False)

    @property
    def likes_count(self):
        return self.like_set.count()

    def __str__(self):
        return self.body[0:10] + '...'

class Like (models.Model):
    Comment = models.ForeignKey('Comment')
    user = models.ForeignKey(User)
    time = models.DateField(auto_now_add=True)

class BaseActivity (models.Model): #DONE: esm az halate jam kharej beshe  #Done: Base bezaarim tahesh!
    ticket = models.ForeignKey('Ticket', related_name="%(app_label)s_%(class)s_related",
                                related_query_name="%(app_label)s_%(class)s_relateds",)
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related",
                                related_query_name="%(app_label)s_%(class)s_relateds",)
    time = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Referral (BaseActivity):
    reffered_to = models.ManyToManyField(User)

class SetConfirmationLimit (BaseActivity):
    limit_value = models.IntegerField(default = 0)
    need_to_confirmed = models.BooleanField(default = False)

class EditTicket (BaseActivity): #TODO: vaghti edit mikone, noskhe ghabli ro negah dare, injoori hame ro darim!
    new_body = models.TextField()
    new_title = models.CharField(max_length=500)

class ChangeStatus (BaseActivity):
    status = models.CharField(choices = Ticket.STATUS_CHOICES, max_length=15)

class Reopen (BaseActivity):
    new_ticket = models.ForeignKey('Ticket')
