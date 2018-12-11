from django.http import HttpResponse
from django.views import View
from httpsig import HeaderVerifier

class Inbox(View):
    def get(self, request):
        if request.META['HTTP_ACCEPT'].find('json') != -1:
            return get_json(self, request)
        else:
            return get_text(self, request)
    def post(self, request):
        if request.META['HTTP_ACCEPT'].find('json') != -1:
            return post_json(self, request)
        else:
            return post_text(self, request)

    def post_json(self, request):
        # validate signature
        signature_header = request.META.get("HTTP_SIGNATURE", "")

        # store the activity

        return signature_header
