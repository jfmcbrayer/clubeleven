from django.db import models
from django.contrib.postgres import fields
from django.core.serializers.json import DjangoJSONEncoder

class BasePost(models.Model):
    name = models.CharField(max_length=140, null=True)
    media_type = models.CharField(max_length=80, null=True)
    posted_by = models.ForeignKey('BaseActor', models.CASCADE, null=True)
    icon = models.ImageField(null=True)
    image = models.ImageField(null=True)
    json = fields.JSONField(encoder = DjangoJSONEncoder,
                            null=True)

class BaseActor(models.Model):
    display_name = models.CharField(max_length=80)
    profile_url = models.URLField(max_length=2048)
    inbox_url = models.URLField(max_length=2048)
    outbox_url = models.URLField(max_length=2048)
    local_user = models.ForeignKey('self', models.SET_NULL, null=True)
    json = fields.JSONField(encoder = DjangoJSONEncoder, null=True)

class User(models.Model):
    email = models.EmailField(null=True)
    # password?
    # fields needed for alternate auth methods?


class Persona(BaseActor):
    default_visibility = models.CharField(max_length=8,
                                          choices=(("PUB", "Public"),
                                                   ("FL", "Followers only"),
                                                   ("MUT", "Friends only"),
                                                   ("LIST", "Listed people only"),))
    is_searchable = models.BooleanField(default=True)
    avatar = models.ImageField(null=True)

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
