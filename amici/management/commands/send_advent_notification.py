import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from amici.models import (
    Friend,
    # OptOutLink,
)
from amici.utils import get_email_context


class Command(BaseCommand):
    help = 'Sends an Advent Friend notification e-mail'

    def add_arguments(self, parser):
        parser.add_argument(
            '--notification',
            type=int,
            choices=(1, 2),
        )

    def activate_all_friends(self):
        for friend in Friend.objects.filter(active=False):
            friend.active = True
            friend.save()

    # def expire_all_opt_out_links(self):
    #     for link in OptOutLink.objects.filter(expired=False):
    #         link.expired = True
    #         link.save()

    def handle(self, *args, **options):

        notification = options['notification']

        year = datetime.date.today().year
        subject = f'Advent Friends ({year})'

        if notification == 1:
            # cleanup everything for first notification
            self.activate_all_friends()
            # self.expire_all_opt_out_links()

        for friend in Friend.objects.filter(active=True):
            if notification == 1:
                # opt_out_link = OptOutLink.objects.create(
                #     friend = friend,
                # )
                pass
            elif notification == 2:
                # opt_out_link = OptOutLink.objects.filter(
                #     expired=False,
                #     friend=friend,
                # )
                pass

            context = get_email_context(
                recipient_name=friend.display_name,
                notification=notification,
                year=year,
                # opt_out_urlname=opt_out_link.urlname,
            )

            message = render_to_string('amici/templates/email.txt', context)

            # html_message = render_to_string('amici/templates/email.html', context)

            send_mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                message=message,
                # html_message=html_message,
                recipient_list=(friend.email,),
            )

        print('finis')
