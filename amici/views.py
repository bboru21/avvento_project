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

def index(request):
    return HttpResponse("amici")

def opt_out(request, urlname):

    link = get_object_or_404(OptOutLink, urlname=urlname)

    action = request.POST.get('action', 'choose')

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
        { 'link': link, 'action': action, 'urlname': urlname },
    )


    return HttpResponse(f'opt out {urlname}')