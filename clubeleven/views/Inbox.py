from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings as django_settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache, cache_page
from django.urls import reverse
from django.views import View
from httpsig import HeaderVerifier

class Inbox(View):
    def get(self, request):
        if request.META['HTTP_ACCEPT'].find('json') != -1:
            return self.get_json(request)
        else:
            return self.get_text(request)
    def post(self, request):
        if request.META['CONTENT_TYPE'].find('json') != -1:
            return self.post_json(request)
        else:
            return self.post_text(request)

    def post_json(self, request):
        # validate signature
        signature_header = request.META["HTTP_SIGNATURE"]
        key_id, headers, signature = [x.strip().split("=")[1].strip('"')
                                      for x in signature_header.split(",")]

        # store the activity

        return HttpResponse(f'''keyID: {key_id}
headers: {headers}
signature: {signature}''')

    def get_text(self, request):
        return render(request, 'core/inbox.html')

