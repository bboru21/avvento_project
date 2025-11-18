import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from django.core.mail import (
    mail_admins,
    send_mail,
)

from amici.models import (
    Friend,
    FriendList,
)

logger = logging.getLogger(__name__)


def _format_money(n):
    return "${:,}".format(n) if isinstance(n, int) else n


class Command(BaseCommand):

    help = '''
        Sends the Advent Friend notification e-mail with the name of this year's Advent Friend.
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            '-t',
            action='store_true',
            help='runs script without database write, sends email to matching superusers only',
        )
        # parser.add_argument(
        #     '--date',
        #     type=str,
        # )
        parser.add_argument(
            '--cap',
            '-c',
            type=int,
            default=None,
            help='adds a spending limit cap message to email'
        )


    def handle(self, *args, **options):

        superuser_emails = list(User.objects.all().filter(is_superuser=True).values_list('email', flat=True))

        # TODO doesn't currently work
        # if options['date']:
        #     friends = FriendList.objects.filter(date=options['date']).values_list('giver', 'recipient')
        # else:
        friend_list = FriendList.get_latest_list()

        print(f'Preparing to send email for {len(friend_list)} contacts...')
        
        cap = options['cap']
        cap_message = f'As a reminder, please try to keep gifts within the {_format_money(cap)} budget.' if cap else ''

        try:


            for item in friend_list:

                giver = item.giver
                recipient = item.recipient

                giver_name = giver.alt_name
                if not giver_name:
                    giver_name = giver.first_name

                recipient_first_name = recipient.first_name
                recipient_last_name = recipient.last_name
                recipient_name = f'{recipient_first_name} {recipient_last_name}'

                recipient_alt_name = recipient.alt_name
                if recipient_alt_name:
                    recipient_name = f'{recipient_name} ({recipient_alt_name})'

                message = f"""
                    Hi {giver_name},

                    Your Advent Friend this year is {recipient_name}. 
                    {cap_message}

                    Wishing you a blessed Advent season!

                    --{settings.DEFAULT_FROM_EMAIL_NAME}
                """

                # send email only if not a test, or if the user email is that of a superuser (for message verification)
                if not options['test'] or (giver.email in superuser_emails):
                    subject = 'Advent Friend (Test)' if options['test'] else 'Advent Friend'
                    send_mail(
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        subject=subject,
                        message=message,
                        recipient_list=(giver.email,)
                    )

        except BaseException as error:
            logger.error(str(error))
            mail_admins(
                subject="Amici dell'Avvento Error",
                message=str(error),
            )

        mail_admins(
            subject="Amici dell'Avvento Success",
            message="Script ran successfully.",
        )
        logger.info('finis')
