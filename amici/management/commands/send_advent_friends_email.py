import logging

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


class Command(BaseCommand):

    help = '''
        Sends the Advent Friend notification e-mail with the name of this year's Advent Friend.
    '''

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='runs script without database write or sending email',
        )
        parser.add_argument(
            '--date',
            type=str,
        )


    def handle(self, *args, **options):

        # TODO doesn't currently work
        # if options['date']:
        #     friends = FriendList.objects.filter(date=options['date']).values_list('giver', 'recipient')
        # else:
        friend_list = FriendList.get_latest_list()

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

                    Your Advent friend is: {recipient_name}

                    Wishing you a Blessed Advent!

                    {settings.DEFAULT_FROM_EMAIL_NAME}
                """
                # print(message)
                # logger.debug(message)

                if not options['test']:
                    send_mail(
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        subject='Advent Friend',
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
