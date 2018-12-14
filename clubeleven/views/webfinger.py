from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings as django_settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_page
from django.urls import reverse
from clubeleven_models.models import Persona
import re
import json


def webfinger(request):
    resource = request.GET.get("resource")
    if not resource:
        return Http404()
    match = re.compile(r'acct:(.*)@(.*)').match(resource)
    if not match:
        return Http404()
    try:
        user = Persona.objects.get(shortname = match.group(1))
    except Persona.DoesNotExist:
        return Http404()

    retjson = { "subject": resource,
                "aliases": [user.profile_url, ],
                "links": [
                    {
                        "rel": "http://webfinger.net/rel/profile-page",
                        "type": "text/html",
                        "href": user.profile_url
                    },
                    {
                        "rel": "self",
                        "type": "application/activity+json",
                        "href": user.profile_url
                    }
                ]
    }
    return HttpResponse(json.dumps(retjson), content_type="application/json")
