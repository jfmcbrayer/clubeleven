from django.db import models

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

