from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class APResponseMixin():
    """
    Mixin to determine whether to send a regular response or an
    ActivityPub response or a normal HTML response.
    """
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

@method_decorator(login_required, name='dispatch')
class Inbox(View):
    def get(self, request):
        return render(request, "core/inbox.html")

    def post(self, request):
        pass

