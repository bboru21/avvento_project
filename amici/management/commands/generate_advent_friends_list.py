from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from amici_dell_avvento.models import (
    Friend,
    FriendList,
)
from random import shuffle
from util.util import Email
from backoff import on_exception, expo


EMAIL = Email(
    email = settings.SENDER_EMAIL,
    password = settings.SENDER_EMAIL_PASSWORD,
    host = settings.SENDER_EMAIL_HOST,
    port = settings.SENDER_EMAIL_PORT,
)

class InvalidFriendListException(Exception):
    """Raised when an invalid Advent Friend List is detected """
    def __init__(self, item1, item2):
        self.item1 = item1
        self.item2 = item2

    def __str__(self):
        return str('%s is an invalid friend for %s' % (self.item2, self.item1))

def validate_friend_list(matches):
    for m1, m2 in matches:
        if not is_valid_friend(m1, m2):
            raise InvalidFriendListException(m1, m2)
            EMAIL.send(

            )
            return False
    return True

def is_valid_friend(a, b):
        if a and b and a['id'] not in [b['id'], b['spouse']]:
            return True
        return False

        return False

class Command(BaseCommand):
    help = 'Generates the Advent Friend List'
    pool = []

    def get_friend(self, contact):
        shuffle(self.pool)
        for person in self.pool:
            if is_valid_friend(person, contact):
                self.pool.remove(person)
                return person
        return None

    '''
        Use backoff package to retry if we get a list that has someone without an advent friend
    '''
    @on_exception(expo, InvalidFriendListException, max_tries=3)
    def handle(self, *args, **options):
            friends = []
            contacts = Friend.objects \
                .filter(active=True) \
                .values('id', 'first_name', 'last_name', 'alt_name', 'email', 'spouse')

            self.pool = list(contacts).copy()

            for contact in contacts:
                friend = self.get_friend(contact)
                friends.append([contact, friend])

            validate_friend_list(friends)

            try:
                with transaction.atomic():
                    for [g, r] in friends:

                        giver = Friend.objects.get( id=int(g.get('id')) )
                        recipient = Friend.objects.get( id=int(r.get('id')) )

                        f = FriendList( giver=giver, recipient=recipient )
                        f.save()

                for [g, r] in friends:

                    giver_name = g.get('alt_name')
                    if not giver_name:
                        giver_name = g.get('first_name')

                    recipient_name = '%s %s' % (r.get('first_name'), r.get('last_name'))
                    if r.get('alt_name'):
                        recipient_name = '%s (%s)' % (recipient_name, r.get('alt_name'))

                    EMAIL.send(
                        recipient_email=g.get('email'),
                        subject='Advent Friend',
                        message = """
                            Hi %s,

                            Your Advent friend is: %s

                            Happy Advent!

                            --Bryan
                        """ % (giver_name, recipient_name))
            except BaseException as error:
                print(str(error))
                EMAIL.send(
                    settings.ADMIN_EMAIL,
                    subject="Amici dell'Avvento Error",
                    message=str(error),
                    send_email_override=True,
                )

            EMAIL.send(
                settings.ADMIN_EMAIL,
                subject="Amici dell'Avvento Success",
                message="Script ran successfully.",
                send_email_override=True,
            )
            print('finis')