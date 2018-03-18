from django.http import JsonResponse
from django.views import View

class APResponseMixin():
    """
    Mixin to determine whether to send a regular response or an
    ActivityPub response or a normal HTML response.
    """
    def get(self, request, *args, **kwargs):
        pass

