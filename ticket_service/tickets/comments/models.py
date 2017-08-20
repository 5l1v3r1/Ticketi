from django.db import models
from django.contrib.auth.models import User

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
