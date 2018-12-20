import requests, json, hashlib, httpsig, base64
from clubeleven_models.models import BaseActor, Persona
from clubeleven.constants import ACTIVITY_TYPES
from django.urls import reverse
from django.utils import timezone
from email.utils import formatdate
from time import mktime
from urllib.parse import urlparse
from uuid import uuid4
from webfinger import finger
from pdb import set_trace


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
        print(profile)
        return BaseActor.objects.get(profile_url = profile)
    except BaseActor.DoesNotExist:
        #     Else, fetch it and create a BaseActor object.
        result = requests.get(profile, headers={"Accept": "application/ld+json"})
        actor = result.json()

        if actor['type'] == 'Person':
            new_actor = Persona()
        else:
            new_actor = BaseActor()
        new_actor.inbox = actor['inbox']
        new_actor.outbox = actor['outbox']
        new_actor.public_key = actor['publicKey']['publicKeyPem']
        new_actor.profile_url = actor['url']
        new_actor.display_name = actor['name']
        new_actor.shortname = actor['preferredUsername']
        new_actor.summary = actor['summary']
        new_actor.ap_type = actor['type']
        #new_actor.json = result.text
        # Get their icon and image and store locally
        # new_actor.icon = actor['icon']
        # new_actor.image = actor['']
        new_actor.save()
        return new_actor

def deliver_remote(to, actor, message, cc=[]):
    """Deliver a message to one or more remote users.

    `to` is a list of BaseActor objects; so is `cc`.
    `actor` is a BaseActor object.
    `message` is a python dictionary corresponding to an ActivityPub message.
    """
    recipients = to + cc

    if "@context" not in message.keys():
        message["@context"] = ["https://www.w3.org/ns/activitystreams",
                               "https://w3id.org/security/v1"]

    if "id" not in message.keys():
        message["id"] = reverse("message", kwargs={"uuid": str(uuid4())});

    # FIXME: save the message. Needs to be retrievable by uuid

    if message["type"] not in ACTIVITY_TYPES:
        new_message = {
            "@context": ["https://www.w3.org/ns/activitystreams",
                          "https://w3id.org/security/v1"],
            "id": reverse("message", kwargs={"uuid": str(uuid4())}) + "/create",
            "actor": actor.profile_url,
            "object": message
        }
    else:
        new_message = message

    for recipient in recipients:
        # Now deliver to inbox:
        payload = json.dumps(new_message)
        new_digest = hashlib.sha256()
        new_digest.update(payload.encode("utf-8"))
        new_digest = base64.encodestring(new_digest.digest()).strip()
        request_headers = {}
        request_headers['date'] = formatdate(timeval = mktime(timezone.now().timetuple()),
                                             localtime=False, usegmt=True)
        request_headers["digest"] = (b"SHA-256=" + new_digest).decode("UTF-8")
        request_headers["host"] = urlparse(recipient.inbox_url).hostname
        set_trace()

        hs = httpsig.HeaderSigner(actor.profile_url + "#mainkey",
                                  actor.private_key,
                                  algorithm="rsa-sha256",
                                  headers = ['(request-target)', 'host', 'date',
                                             'digest'],
                                  sign_header="signature")
        set_trace()
        signed_headers = hs.sign(request_headers,
                                 host = urlparse(recipient.inbox_url).hostname,
                                 method="POST",
                                 path=urlparse(recipient.inbox_url).path)
        signed_headers['content-type'] = "application/ld+json"
        
