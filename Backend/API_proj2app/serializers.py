#/[app]/serializers.py
# from http://lucasjackson.io/realtime-ios-chat-with-django/

from rest_framework import serializers

from . import models

# this handles the information for the user that will be sent back to the client (username and hash_id).

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='hash_id',read_only=True)

    class Meta:
        model = models.User
        fields = ('id','username')
