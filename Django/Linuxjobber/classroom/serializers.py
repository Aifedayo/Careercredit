from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class DjangoStudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required= True)
    email = serializers.EmailField(required=False, allow_blank=True)
    
   
    class Meta:
        model = DjangoStudent
        fields = ('id', 'username','email')





