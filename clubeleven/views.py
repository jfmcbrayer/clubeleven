from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

class APResponseMixin():
    """
    Mixin to determine whether to send a regular response or an
    ActivityPub response or a normal HTML response.
    """
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

@login_required
class Inbox(View):
    def get(self, request):
        return render(request, "core/inbox.html")

    def post(self, request):
        pass

