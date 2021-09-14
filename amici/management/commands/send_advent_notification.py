from django.core.management.base import BaseCommand
from django.conf import settings
from amici.models import Friend
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Sends an Advent Friend noticication e-mail'

    def add_arguments(self, parser):
        parser.add_argument('notification', type=int, choices=(1, 2))

    def handle(self, *args, **options):

        notification = options['notification']

        subject = 'Advent Friends'

        for friend in Friend.objects.filter(active=True):
            if notification == 1:
                message = f"""
                    Hi {friend.display_name},

                    Advent is just around the corner, and we'll be drawing
                    names in just a few days! Please let me know ASAP if you
                    don't want to participate. Otherwise on November 11th I
                    will email you your secret name!

                    --Bryan
                """
            elif notification == 2:
                message = f"""
                    Hi {friend.display_name},

                    Just a reminder that we'll be drawing names tomorrow, so
                    please let me know ASAP if you don't want to participate!

                    --Bryan
                """

            send_mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                message=message,
                recipient_list=(friend.email,),
            )

        print('finis')
