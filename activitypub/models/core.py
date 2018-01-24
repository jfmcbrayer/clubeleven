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
    preview = models.ForeignKey(Common, models.SET_NULL, null=True,
                                related_name = "previews",
                                related_query_name = "preview")

    object_type = "Link"

class PubObject(Common):
    pub_id = models.URLField()
    attachment = models.ForeignKey(Common, models.SET_NULL, null=True)
    attributed_to = models.ForeignKey(Common, models.SET_NULL, null=True)
    audience = models.ForeignKey(Common, models.SET_NULL, null=True)
    content = models.TextField(null=True)
    end_time = models.DateTimeField(null=True)
    generator = models.ForeignKey(Common, models.SET_NULL, null=True)
    icon = models.ImageField(null=True)
    image = models.ImageField(null=True)
    in_reply_to = models.ForeignKey(Common, models.SET_NULL, null=True)
    location = models.ForeignKey(Common, models.SET_NULL, null=True)
    preview = models.ForeignKey(Common, models.SET_NULL, null=True)
    published = models.DateTimeField(null=True, auto_now_add=True)
    # replies = models.ForeignKey(Collection, models.SET_NULL, null=True)
    source = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(null=True)
    summary = models.TextField(null=True, blank=True)
    tag = models.ForeignKey(Common, models.SET_NULL, null=True)
    updated = models.DateTimeField(null=True)
    url = models.ForeignKey(Link, models.SET_NULL, null=True)
    to = models.ForeignKey(Common, models.SET_NULL, null=True)
    bto = models.ForeignKey(Common, models.SET_NULL, null=True)
    cc = models.ForeignKey(Common, models.SET_NULL, null=True)
    bcc = models.ForeignKey(Common, models.SET_NULL, null=True)
    duration = models.DurationField(null=True)

    object_type = "Object"

