from django.db import models
from django.conf import settings
from django.contrib.postgres import fields
from django.core.serializers.json import DjangoJSONEncoder
from mimetypes import guess_type
import json

class BasePost(models.Model):
    name = models.CharField(max_length=140, null=True)
    media_type = models.CharField(max_length=80, null=True)
    posted_by = models.ForeignKey('BaseActor', models.CASCADE, null=True)
    icon = models.ImageField(null=True, upload_to='uploads/%Y/%m/%d/')
    image = models.ImageField(null=True, upload_to='uploads/%Y/%m/%d/')
    json = fields.JSONField(encoder = DjangoJSONEncoder,
                            null=True, blank=True)
    def __str__(self):
        return self.name

class BaseActor(models.Model):
    display_name = models.CharField(max_length=80)
    profile_url = models.URLField(max_length=2048, unique=True)
    inbox_url = models.URLField(max_length=2048)
    outbox_url = models.URLField(max_length=2048)
    icon_url = models.URLField(max_length=2048, null=True, blank=True)
    image_url = models.URLField(max_length=2048, null=True, blank=True)
    icon = models.ImageField(null=True, upload_to='uploads/%Y/%m/%d/')
    image = models.ImageField(null=True, upload_to='uploads/%Y/%m/%d/')
    ap_type = models.CharField(max_length=80, null=True, blank=True)
    local_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, null=True)
    json = fields.JSONField(encoder = DjangoJSONEncoder, null=True, blank=True)
    followers = models.ManyToManyField('self', related_name='followers', blank=True)
    follows = models.ManyToManyField('self',  related_name='follows', blank=True)
    public_key = models.TextField(blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.display_name

class Persona(BaseActor):
    default_visibility = models.CharField(max_length=8,
                                          choices=(("PUB", "Public"),
                                                   ("FL", "Followers only"),
                                                   ("MUT", "Friends only"),
                                                   ("LIST", "Listed people only"),))
    is_searchable = models.BooleanField(default=True)
    shortname = models.SlugField()

    def to_json(self):
        return json.dumps( {
            '@context': ["https://www.w3.org/ns/activitystreams",
                         "https://w3id.org/security/v1"],
            "id": self.profile_url,
            "type": "Person",
            "preferredUsername": self.shortname,
            "inbox": self.inbox_url,
            "outbox": self.outbox_url,
            "publicKey": {
                "id": self.profile_url + "#main-key",
                "owner": self.profile_url,
                "publicKeyPem": self.public_key
            },
            "summary": self.summary,
            "icon": {
                "type": "Image",
                "mediaType": guess_type(self.icon.name),
                "url": self.profile_url + "/icon"
            }
        })

class Link(BasePost):
    href = models.URLField(max_length=2048)
    hreflang = models.CharField(max_length=8, null=True)
    height = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    preview = models.TextField()

class Post(BasePost):
    content = models.TextField()
    source = models.TextField()

class MediaPost(Post):
    media = models.FileField()

class Comment(Post):
    conversation = models.ForeignKey(Post, models.CASCADE, related_name="comments")
    parent = models.ForeignKey(Post, models.CASCADE, related_name="children")

class Reaction(Comment):
    type = models.CharField(max_length=8,
                            choices=(("LIKE", "Like"),
                                     ("DISLIKE", "Dislike"),
                                     ("SEEN", "Seen")))
    # This is weird, but emoji constructed with ZWJ characters can be quite long,
    # though normal emoji are one character. I'm leaving this quite large, because
    # the perfectly reasonable emojo "black woman kissing black woman" takes like
    # 9 codepoints.
    emojo = models.CharField(max_length=16, null=True)
    shortcode = models.CharField(max_length=16, null=True)

class InspectableMessage(models.Model):
    """A simple class for storing a message received from an AP server so I can
    inspect it and deal with it manually"""
    signature = models.CharField(max_length=4096, null=True, blank=True)
    signature_checked = models.BooleanField(default=False)
    signature_check_passed = models.BooleanField(null=True, blank=True)
    json = models.TextField(null=True, blank=True)
    host = models.CharField(max_length=2048, null=True, blank=True)
    date = models.CharField(max_length=80, null=True, blank=True)
    digest = models.TextField(null=True, blank=True)
    content_type = models.CharField(max_length=1024, null=True, blank=True)
    request_target = models.CharField(max_length=4096, null=True, blank=True)
