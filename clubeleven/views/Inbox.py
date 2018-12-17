from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings as django_settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_page
from django.urls import reverse
from django.views import View
from httpsig import HeaderVerifier
from django.utils import timezone
from clubeleven_models.models.core import InspectableMessage
import sys
import json


def inbox(request, username):
    if request.method == 'GET':
        if request.META['HTTP_ACCEPT'].find('json') != -1:
            return get_json(request, username)
        else:
            return get_text(request, username)
    if request.method == 'POST':
        if request.META['CONTENT_TYPE'].find('json') != -1:
            return post_json(request, username)
        else:
            return post_text(request, username)

def post_json(request, username):
    # validate signature
    signature_header = request.META["HTTP_SIGNATURE"]
    # headers="(request-target) host date digest content-type"
    # keyId="https://anticapitalist.party/users/gcupc#main-key",algorithm="rsa-sha256",headers="(request-target) host date digest content-type",signature="0XyzGimcjiZmuwiiQPRmQxPDBffYxxqJY6nGXPtZa1ooHy9oqA/Q0oTsUDGF9FIC84Ekbagqj15W2b+sPksK7ogTb/jMZr4x36zekMLlhTEcbqXOCJB35xJMLhDY5k68GMKeOZqSHCmBfNkQltcxSqFBJQRY+SDd+zdsUgQRQbEaKRFk/FIv2j+YhbLOHFNutD/WNgnR+PTR1e59FHQBI2Bdmx2Pby0MQz1wTRSjfpHYUpcQiiwWbUWnIAdCz5bTO1MpbOj1uzGAI8BsBixt9YW24fn+c86VVKlJ8AILPp1DFpEeELV1SyzLYPDRoctI6EObpD+FaAwjTAC+Ilytiw=="
    key_id, algorithm, headers, signature = [x.strip().split("=")[1].strip('"')
                                             for x in signature_header.split(",")]
    # store the activity
    message = InspectableMessage()
    message.json = request.body.decode("UTF-8")
    message.signature = signature_header
    message.host = request.get_host()
    message.date = request.META['HTTP_DATE']
    message.digest = request.META.get("HTTP_DIGEST", None)
    message.content_type = request.META['CONTENT_TYPE']
    message.request_target = "(request target): " + request.method.lower() + " " + request.path
    message.save()

    return HttpResponse("OK")

def get_text(request, username):
    return render(request, 'core/inbox.html')

