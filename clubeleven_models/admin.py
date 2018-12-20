from .models import Persona, Post, InspectableMessage, BaseActor
from django.contrib import admin

admin.site.register(BaseActor)
admin.site.register(Persona)
admin.site.register(Post)
admin.site.register(InspectableMessage)

