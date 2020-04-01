from rest_framework import serializers
from .models import User, ChatMessageWithProfile

class MessageSerializer(serializers.Serializer):
   """Your data serializer, define your fields here."""
   username = serializers.CharField(max_length=200)
   content = serializers.CharField(max_length=200)
   profile_img = serializers.CharField(max_length=200)
   timestamp = serializers.CharField(max_length=20)
   the_type = serializers.CharField(max_length=50)
#    likes = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','profile_img')

class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    content = serializers.CharField(source='message')
    class Meta:
        model = ChatMessageWithProfile
        fields = ('id','user','content','the_type','timestamp')

