from django.db import models
from django.conf import settings
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
import urllib
import json
from . import helper # we created this
import base64


class Base64Field(models.TextField):
    def contribute_to_class(self, cls, name):
        if self.db_column is None:
            self.db_column = name
        self.field_name = name
        super(Base64Field, self).contribute_to_class(cls, self.field_name)
        setattr(cls, name, property(self.get_data, self.set_data))

    def get_data(self, obj):
        return base64.decodestring(getattr(obj, self.field_name))

    def set_data(self, obj, data):
        setattr(obj, self.field_name, base64.encodestring(data))


# helpful link: https://www.digitalocean.com/community/tutorials/how-to-create-django-models
# The User model. The user_id is automatically generated
class User(AbstractUser):

    hash_id = models.CharField(max_length=32, default=helper.create_hash, unique=True)

    firstname = models.CharField(max_length=30, default="none")
    lastname = models.CharField(max_length=30, default="none")

    # username and password already in AbstractUser
    #username = models.CharField(max_length=30, default="none", unique=True)
    #password = models.CharField(max_length=30, default="none")
    # for displaying a user objects
    def __str__(self):
        return self.username + " (name: " + self.firstname + " " + self.lastname + ")"

class Memory(models.Model):
    hash_id = models.CharField(max_length=32)
    title = models.CharField(max_length=255, default="none")
    text = models.TextField(default="none")
    image = models.TextField(default="none") #Base64Field() # models.ImageField(upload_to='images/') --> alternatively: https://wsvincent.com/django-image-uploads/
    date = models.CharField(max_length=255, default="none")

    def __str__(self):

             return "title: " + self.title + " date: " + str(self.date) + " (id:" + str(self.id) + ")"

    # orders posts by date created : https://www.digitalocean.com/community/tutorials/how-to-create-django-models
    class Meta:
        ordering = ['date']

        def __unicode__(self):
            return self.title
