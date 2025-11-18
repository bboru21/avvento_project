from random import shuffle
import logging

from backoff import on_exception, expo

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from amici.models import (
    Friend,
    FriendList,
)

logger = logging.getLogger(__name__)

PREVIOUS_LIST_DICT = {
    str(i.giver.pk): i.recipient.pk for i in FriendList.get_latest_list()
}

MAX_TRIES = settings.MAX_GENERATE_LIST_RETRIES + 1

class InvalidFriendListException(Exception):
    """Raised when an invalid Advent Friend List is detected """
    def __init__(self, item1, item2):
        self.item1 = item1
        self.item2 = item2

    def __str__(self):
        return f'{self.item2} is an invalid friend for {self.item1}'


def validate_friend_list(matches):
    for m1, m2 in matches:
        if not is_valid_friend(m1, m2):
            raise InvalidFriendListException(m1, m2)
            return False
    return True


def is_valid_friend(a, b):
    if b is not None:
        # exclude themselves, spouse and friend from previous year
        excluded_ids = [
            b['id'],
            b['spouse'],
            PREVIOUS_LIST_DICT.get(str(b['id']), 0),
        ]
        if a and b and a['id'] not in excluded_ids:
            return True
        return False

    return False


class Command(BaseCommand):

    help = '''
        Generates an Advent Friend list from active participants (Friend), and
        creates a spreadsheet and e-mails participants.
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='runs script without database write or sending email',
        )

    pool = []

    def get_friend(self, contact):
        shuffle(self.pool)
        for person in self.pool:
            if is_valid_friend(person, contact):
                self.pool.remove(person)
                return person
        return None

    '''
        Use backoff package to retry if we get a list that has someone without
        an advent friend
    '''
    @on_exception(expo, InvalidFriendListException, max_tries=MAX_TRIES)
    def handle(self, *args, **options):

        friends = []
        contacts = Friend.objects \
            .filter(active=True) \
            .values(
                'id',
                'first_name',
                'last_name',
                'alt_name',
                'email',
                'spouse',
            )

        self.pool = list(contacts).copy()

        for contact in contacts:
            friend = self.get_friend(contact)
            friends.append([contact, friend])

        validate_friend_list(friends)

        try:
            with transaction.atomic():
                for [g, r] in friends:

                    giver = Friend.objects.get(id=int(g.get('id')))
                    recipient = Friend.objects.get(id=int(r.get('id')))

                    f = FriendList(giver=giver, recipient=recipient)
                    if not options['test']:
                        f.save()

        except BaseException as error:
            logger.error(str(error))
            # mail_admins(
            #     subject="Amici dell'Avvento Error",
            #     message=str(error),
            # )

        # mail_admins(
        #     subject="Amici dell'Avvento Success",
        #     message="Script ran successfully.",
        # )
        logger.info('finis')
