from django.db import models

class BasePost(models.Model):
    name = models.CharField(max_length=80, null=True)
    media_type = models.CharField(max_length=80, null=True)

class BaseActor(models.Model):
    display_name = models.CharField(max_length=80)
    profile_url = models.URLField(max_length=2048)
    inbox_url = models.URLField(max_length=2048)
    outbox_url = models.URLField(max_length=2048)
    local_user = models.ForeignKey('BaseActor', models.SET_NULL, null=True)

class User(models.Model):
    email = models.EmailField(null=True)
    # password?
    # fields needed for alternate auth methods?


class Persona(BaseActor):
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    default_visibility = models.CharField(choices=(("PUB", "Public"),
                                                   ("FL", "Followers only"),
                                                   ("MUT", "Friends only"),
                                                   ("LIST", "Listed people only"),))
    is_searchable = models.BooleanField(default=True)
