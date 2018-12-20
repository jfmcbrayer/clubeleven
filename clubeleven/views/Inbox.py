from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings as django_settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_page
from django.urls import reverse
from django.views import View
from httpsig import HeaderVerifier
from django.utils import timezone
from clubeleven_models.models import InspectableMessage, Persona
import sys
import json
import requests
import hashlib
import base64

def inbox(request, username):
    user = get_object_or_404(Persona, shortname=username)
    if not user.local_user:
        raise Http404()
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
    sig_result = verify_signature(request, key_id, headers.split(" "), signature_header)

    # store the activity
    message = InspectableMessage()
    message.json = request.body.decode("UTF-8")
    message.signature = signature_header
    message.host = request.get_host()
    message.date = request.META['HTTP_DATE']
    message.digest = request.META.get("HTTP_DIGEST", None)
    message.content_type = request.META['CONTENT_TYPE']
    message.request_target = "(request target): " + request.method.lower() + " " + request.path
    message.signature_checked = True
    message.signature_check_passed = sig_result
    message.save()

    return HttpResponse("OK")

def get_text(request, username):
    return render(request, 'core/inbox.html')

def verify_signature(request, key_id, headers, signature):
    # Fetch the key
    req = requests.get(key_id, headers={"Accept": "application/ld+json"})
    pubkey = req.json()["publicKey"]["publicKeyPem"]

    #verify
    digest = request.META.get("HTTP_DIGEST", None)
    request_headers =  {
        "signature": signature,
        "host": request.get_host(),
        "date": request.META['HTTP_DATE'],
        "content-type": request.META["CONTENT_TYPE"]
    }
    if digest:
        new_digest = hashlib.sha256()
        new_digest.update(request.body)
        new_digest = base64.encodestring(new_digest.digest()).strip()
        request_headers["digest"] = (b"SHA-256=" + new_digest).decode("UTF-8")

    # TODO: check date stamp to avoid replay attacks
    # TODO: check attribution

    hv = HeaderVerifier(request_headers, pubkey, headers, request.method,
                        request.path, sign_header='Signature')
    return hv.verify()
