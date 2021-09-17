from django.db import models
import datetime

import smtplib
from email.mime.text import MIMEText
import uuid


class Friend(models.Model):
    first_name = models.CharField('first name', max_length=250)
    last_name = models.CharField('last name', max_length=250)
    alt_name = models.CharField('nick name', max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    spouse = models.OneToOneField('self', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def display_name(self):
        if self.alt_name:
            return self.alt_name
        return self.first_name

    @property
    def display_fullname(self):
        return '{} {}'.format(self.display_name, self.last_name)

    def __str__(self):
        return self.display_fullname


class FriendList(models.Model):
    date = models.DateField(auto_now=True)
    giver = models.ForeignKey(Friend, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Friend, related_name='recipient', on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {} -> {}'.format(self.date.year, self.giver.display_fullname, self.recipient.display_fullname)

def _generate_hex():
    return uuid.uuid1().hex


class OptOutLink(models.Model):
    urlname = models.CharField(
        max_length=32,
        default=_generate_hex,
    )
    create_date = models.DateField(auto_now=True)
    expired = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    friend = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        related_name='opt_out_links',
    )

    def __str__(self):
        return f'{self.friend.display_fullname} - {self.urlname}'
