from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from amici_dell_avvento.models import Friend
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Sends an Advent Friend noticication e-mail'

    def add_arguments(self, parser):
        parser.add_argument('notification', type=int, choices=(1,2))

    def handle(self, *args, **options):

        notification = options['notification']

        subject = 'Advent Friends'

        for friend in Friend.objects.filter(active=True):
            if notification == 1:
                message = """
                    Hi %s,
                    Advent is just around the corner, and we'll be drawing names in just a few days! Please let me know ASAP if you don't want to participate. Otherwise on November 11th I will email you your secret name!
                    --Bryan
                """ % friend.display_name
            elif notification == 2:
                message = """
                    Hi %s,
                    Just a reminder that we'll be drawing names tomorrow, so please let me know ASAP if you don't want to participate!
                    --Bryan
                """ % friend.display_name

            send_mail(
                subject=subject,
                message=message,
                recipient_list=[recipient_email=friend.email],
                fail_silently=False,
            )

        print('finis')