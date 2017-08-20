# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import json
from django.core.files import File
import urllib

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    post = models.CharField(max_length = 100)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @property
    def get_profile_pics(self, profile_pic):
        return profile_pic.pic_path

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
    body = models.TextField()
    addressed_users = models.ManyToManyField(User)
    parent_ticket = models.ForeignKey('Ticket')

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

class ProfilePic(models.Model):
    pic = models.ImageField(upload_to='profile_pictures/', default = 'profile_pictures/None/no-image.jpg')
    pic_path =  json.dumps(unicode('pic'))
    user = models.OneToOneField(User, default=None, related_name='pic_user')
    def cache(self):
        result = urllib.urlretrieve(self.url)
        self.pic.save(
            os.path.basename(self.url),
            File(open(result[0]))
        )
        self.save()

class BaseAttachment (models.Model):
    pic = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    description = models.TextField(null = True, blank = True)
    class Meta:
        abstract = True

    def cache(self):
        result = urllib.urlretrieve(self.url)
        self.pic.save(
            os.path.basename(self.url),
            File(open(result[0]))
        )
        self.save()

class PublicAttachment (BaseAttachment): #DONE: esm az halate jam kharej beshe
    ticket = models.ForeignKey('Ticket')

class PrivateAttachment (BaseAttachment): #DONE: esm az halate jam kharej beshe
    ticket = models.ForeignKey('PrivateTicket')

class Comment (models.Model):
    body = models.TextField()
    user = models.ForeignKey(User)
    ticket = models.ForeignKey('Ticket')
    creation_time = models.DateField(auto_now_add=True)
    parent = models.ForeignKey('Comment', default = None, null = True, blank = True)
    being_unknown = models.BooleanField(default = False)
    verified = models.BooleanField(default = False)
    deleted = models.BooleanField(default = False)
    edited = models.BooleanField(default = False)

    @property
    def likes_num(self):
        return self.like_set.count()

    def __str__(self):
        return self.body[0:10] + '...'

class Like (models.Model):
    comment = models.ForeignKey('Comment')
    user = models.ForeignKey(User)
    time = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'comment']

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

class EditTicketActivity (BaseActivity): #TODO: vaghti edit mikone, noskhe ghabli ro negah dare, injoori hame ro darim!
    prev_title = models.CharField(max_length=500)
    prev_body = models.TextField()

class ChangeStatusActivity (BaseActivity):
    status = models.CharField(choices = Ticket.STATUS_CHOICES, max_length=15)

class ReopenActivity (BaseActivity):
    new_ticket = models.ForeignKey('Ticket')
