from .core import BaseActor, BasePost
from django.db import models

class Event(BaseActor):
    owner = models.ForeignKey('BaseActor', models.DELETE, null=False)
    # Add all the scheduling and location fields here.

class Invite(models.Model):
    event = models.ForeignKey('Event', models.DELETE, null=False)
    recipient = models.ForeignKey('BaseActor', models.DELETE, null=False)
    response = models.ForeignKey('BasePost', models.SET_NULL, nullTrue)
