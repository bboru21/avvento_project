from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.http import HttpResponse
from django.core.mail import mail_admins

from .models import OptOutLink

def index(request):
    return HttpResponse("amici")

def opt_out(request, urlname):

    link = get_object_or_404(OptOutLink, urlname=urlname)

    action = request.POST.get('action', 'choose')

    if action == 'confirm':
        # TODO add logic to expire OptOutLink, deactivate Friend
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