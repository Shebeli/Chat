from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class ChatUser(AbstractUser):
    first_name = models.CharField(max_length=25, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    display_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    chat_other_user = models.ManyToManyField('self', blank=True, through='PrivateChat')
    REQUIRED_FIELDS = []


class PrivateChat(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='first_user')
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='second_user')
    date_created = models.DateTimeField(auto_now=True)
    blocked = models.BooleanField(default=False)


class PrivateChatMsg(models.Model):
    PC = models.ForeignKey(PrivateChat, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='senders')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='receivers')
    message = models.TextField()
    time_sent = models.TimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


class Group(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='creators')
    member = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    member_count = models.PositiveIntegerField(default=1)


class GroupChatMsg(models.Model):
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    message = models.TextField()
    time_sent = models.TimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

