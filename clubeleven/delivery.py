import requests
from brutaldon_models.models import BaseActor, Persona
 from urllib.parse import urlparse
 from webfinger import finger


def resolve_actor(actor):
    """Resolve a string representing an Actor to a BaseActor object"""
    # If it looks like @foo@server or foo@server, look the profile with webfinger
    if "@" in actor:
        if actor.startswith("@"):
            actor = actor[1:]
        profile = finger("acct:"+actor).rel('self')
    else: # Check that it looks like a URL 
        try:
            urlparse(actor)
            profile = actor
        except ValueError:
            raise BaseActor.DoesNotExist
    # See if the profile is in our local database as a BaseActor
    #     If so, return it (maybe update it?).
    try:
        return BaseActor.objects.get(profile_url = profile)
    except BaseActor.DoesNotExist:
        #     Else, fetch it and create a BaseActor object.
        actor = requests.get(profile, headers={"Accept": "application/ld+json"}).json()

        new_actor = BaseActor()
        new_actor.inbox = actor['inbox']
        new_actor.outbox = actor['outbox']
        new_actor.save()
        return new_actor

def deliver_remote(to, cc, actor, message):
    """Deliver a message to one or more remote users.

    `to` is a list of BaseActor objects; so is `cc`.
    `actor` is a BaseActor object.
    `message` is a python dictionary corresponding to an ActivityPub message.
    """
    recipients = to + cc
    for recipient in recipients:
        # Now deliver to inbox:
        #    If message doesn't have a context, add the default.
        #    If message doesn't have an id, generate one.
        #    If message is not an Activity type, wrap it in a Create.

