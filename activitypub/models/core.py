from django.db import models

## Core classes:
##     Link and Object are supposed to be disjoint, but they are used
##     interchangeably all over the place, and so there's no other way to get
##     the desired characteristics at the table level.

class Common(models.Model):
    name = models.CharField(max_length=80, null=True)
    media_type = models.CharField(max_length=80, null=True)

    object_type = ""
    at_context = "https://w3c.org/ns/activitystreams"

class Link(Common):
    href = models.URLField()
    rel = models.CharField(max_length=20, null=True, blank=True) # add choices
    hreflang = models.CharField(max_length=8, null=True, blank=True)
    height = models.PositiveIntegerField(null=True)
    width = models.PositiveIntegerField(null=True)
    preview = models.ManyToManyField(Common, related_name = "preview_of")

    object_type = "Link"

class PubObject(Common):
    pub_id = models.URLField()
    attachment = models.ForeignKey(Common, models.SET_NULL, null=True,
                                   related_name = "attached_to")
    attributed_to = models.ForeignKey(Common, models.SET_NULL, null=True,
                                      related_name = "attributed_from")
    audience = models.ForeignKey(Common, models.SET_NULL, null=True,
                                 related_name = "audience_for")
    content = models.TextField(null=True)
    end_time = models.DateTimeField(null=True)
    generator = models.ForeignKey(Common, models.SET_NULL, null=True,
                                  related_name = "generated")
    icon = models.ImageField(null=True)
    image = models.ImageField(null=True)
    in_reply_to = models.ForeignKey(Common, models.SET_NULL, null=True,
                                    related_name = "alt_replies",
                                    related_query_name = "alt_reply")
    location = models.ForeignKey(Common, models.SET_NULL, null=True,
                                 related_name = "location_uses",
                                 related_query_name = "location_use")
    preview = models.ForeignKey(Common, models.SET_NULL, null=True,
                                related_name = "preview_for")
    published = models.DateTimeField(null=True, auto_now_add=True)
    # replies = models.ForeignKey(Collection, models.SET_NULL, null=True)
    source = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(null=True)
    summary = models.TextField(null=True, blank=True)
    tag = models.ForeignKey(Common, models.SET_NULL, null=True,
                            related_name = "tagged")
    updated = models.DateTimeField(null=True)
    url = models.ForeignKey(Link, models.SET_NULL, null=True)
    to = models.ManyToManyField(Common, related_name = "to_reverse")
    bto = models.ManyToManyField(Common, related_name = "bto_reverse")
    cc = models.ManyToManyField(Common, related_name = "cc_reverse")
    bcc = models.ManyToManyField(Common, related_name = "bcc_reverse")
    duration = models.DurationField(null=True)

    object_type = "Object"

## Collections:
##     We don't implement all of the collection classes, nor do we implement
##     every specified field on the ones we do implement. Why? All the
##     paging-related items are transient, and they don't need to be
##     represented in a persistent model. A higher level library should wrap
##     these classes to provide paging (and generation of paging-related JSON
##     objects for C2S APIs.)

class Collection(PubObject):
    items = models.ManyToManyField(Common, related_name="in_collections")

    object_type = "Collection"

class OrderedCollection(Collection):
    class Meta:
        ordering = ["-published"]
    object_type = "OrderedCollection"

class Actor(PubObject):
    inbox = models.ForeignKey(OrderedCollection, models.PROTECT, related_name="inbox_owner")
    outbox = models.ForeignKey(OrderedCollection, models.PROTECT, related_name="outbox_owner")
    following = models.ForeignKey(Collection, models.PROTECT, related_name="following_owner")
    followers = models.ForeignKey(Collection, models.PROTECT, related_name="followers_owner")
    liked = models.ForeignKey(Collection, models.PROTECT, related_name="liked_owner")

    object_type = "Actor"

class BaseActivity(PubObject):
    subject = models.ForeignKey(Actor, models.CASCADE) # AP's 'actor' field, but Django
                                                       # does not like it.
    target = models.ForeignKey(PubObject, models.SET_NULL, null=True,
                               related_name="target_of")
    result = models.ForeignKey(PubObject, models.SET_NULL, null=True,
                               related_name="result_of")
    origin = models.ForeignKey(PubObject, models.SET_NULL, null=True,
                               related_name="origin_of")
    instrument = models.ForeignKey(PubObject, models.SET_NULL, null=True,
                                   related_name="instrument_of")

    object_type = "BaseActivity"

class Activity(BaseActivity):
    direct_object = models.ForeignKey(PubObject, models.SET_NULL, null=True,
                                      related_name="direct_object_of")

    object_type = "Activity"

class IntransitiveActivity(BaseActivity):
    object_type = "IntransitiveActivity"






