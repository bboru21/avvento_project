import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from amici.models import (
    Friend,
    OptOutLink,
)


class Command(BaseCommand):
    help = 'Sends an Advent Friend notification e-mail'

    def add_arguments(self, parser):
        parser.add_argument(
            '--notification',
            type=int,
            choices=(1, 2),
        )

    def handle(self, *args, **options):

        notification = options['notification']

        year = datetime.date.today().year
        subject = f'Advent Friends ({year})'

        for friend in Friend.objects.filter(active=True):
            if notification == 1:

                opt_out_link = OptOutLink.objects.create(
                    friend = friend,
                )

                message = f"""
                    Advent is just around the corner, and we'll be drawing
                    names in just a few days! Please let me know ASAP if you
                    don't want to participate. Otherwise on November 11th I
                    will email you your secret name!
                """
            elif notification == 2:

                opt_out_link = OptOutLink.objects.filter(
                    expired=False,
                    friend=friend,
                )
                message = f"""
                    Just a reminder that we'll be drawing names tomorrow, so
                    please let me know ASAP if you don't want to participate!
                """

            context = {
                'notification': notification,
                'recipient_name': friend.display_name,
                'content': message,
                'year': year,
                'link': f'{settings.SITE_URL}amici/opt-out/{opt_out_link.urlname}/',
            }

            message = render_to_string('amici/templates/email.txt', context)

            html_message = render_to_string('amici/templates/email.html', context)

            send_mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                message=message,
                html_message=html_message,
                recipient_list=(friend.email,),
            )

        print('finis')
