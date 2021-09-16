from django.shortcuts import render
from django.http import HttpResponse

from .models import OptOutLink

def index(request):
    return HttpResponse("amici")

def opt_out(request, urlname):
    # opt_out_link = OptOutLink.objects \
    #     .filter(expired=False) \
    #     .get(urlname=urlname)

    return HttpResponse(f'opt out {urlname}')