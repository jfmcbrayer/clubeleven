from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings as django_settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_page
from django.urls import reverse
from django.views import View
from httpsig import HeaderVerifier
from mimetypes import guess_type
from clubeleven_models.models import Persona
from os.path import abspath


def profile(request, username):
    if request.method == 'GET':
        try:
            user = Persona.objects.get(shortname = username)
        except Persona.DoesNotExist:
            return Http404()
        if "json" in request.META['HTTP_ACCEPT']:
            return HttpResponse(user.to_json(), content_type="activity/ld+json")
        else:
            return render(request, "core/profile.html",
                          {"user": user,})

def icon(request, username):
    try:
        user = Persona.objects.get(shortname = username)
    except Persona.DoesNotExist:
        return Http404()
    type = guess_type(user.avatar.name)
    if not type:
        return Http404()
    return HttpResponse(user.avatar.read(), content_type=type[0])
