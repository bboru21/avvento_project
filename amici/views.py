from django.conf import settings
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.http import HttpResponse
from django.core.mail import (
    send_mail,
    mail_admins,
)

from .models import OptOutLink
from .utils import get_email_context

def index(request):
    return HttpResponse("amici")

def preview_email(request, type):

    context = get_email_context(
        recipient_name='Name',
        notification=int(request.GET.get('notification', 1)),
    )

    if type == 'txt':
        template = 'amici/templates/email.txt'
    else:
        template = 'amici/templates/email.html'

    return render(
        request,
        template,
        context,
    )

def opt_out(request, urlname):

    if urlname == 'preview':
        display_name = 'Name'
    else:
        link = get_object_or_404(OptOutLink, urlname=urlname)
        display_name = link.friend.display_name

    action = request.POST.get('action', 'choose')

    context = {
        'action': action,
        'display_name': display_name,
        'urlname': urlname,
    }

    if urlname != 'preview':
        if action == 'confirm':

            # deactivate
            friend = link.friend
            friend.active = False
            friend.save()

           # TODO figure out how to expire the link (while showing confirmation message)

            # send confirmation email to deactivated friend
            send_mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                subject='Advent Friend Opt-Out Successful',
                message=f"""
                    Hi {friend.display_name},

                    Just a confirmation e-mail to let you know your opt out was
                    successful, and that you won't be participating in Advent
                    Friends this year. No further action is required.

                    Blessed Advent and Merry Christmas!

                    {settings.DEFAULT_FROM_EMAIL_NAME}
                """,
                recipient_list=(friend.email,)
            )

            mail_admins(
                "Amici dell'Avvento Opt-Out",
                f"{link.friend.display_fullname} has chosen to opt out.",
            )

    return render(
        request,
        'amici/templates/opt-out.html',
        context,
    )