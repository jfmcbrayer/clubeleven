from .core import BaseActor, BasePost
from django.db import models

class Event(BaseActor):
    owner = models.ForeignKey('Persona', models.CASCADE, null=False,
                              related_name="owner")
    # Add all the scheduling and location fields here.

class Invite(models.Model):
    event = models.ForeignKey('Event', models.CASCADE, null=False,
                              related_name="event")
    recipient = models.ForeignKey('BaseActor', models.CASCADE, null=False,
                                  related_name="recipient")
    response_type = models.CharField(max_length=20,
                                     choices = (("A", "Accept"),
                                                ("R", "Reject"),
                                                ("T", "Tentative")))
    response = models.ForeignKey('BasePost', models.SET_NULL, null=True,
                                 related_name="response")
