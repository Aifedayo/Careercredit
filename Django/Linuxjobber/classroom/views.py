from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from users.models import CustomUser
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import DjangoStudentSerializer


class DjangoStudentViewSet(viewsets.ModelViewSet): 
    # Api end points that access the users
    queryset = DjangoStudent.objects.all()
    serializer_class = DjangoStudentSerializer

    
    def create(self, request):
        user, created = CustomUser.objects.get_or_create(username= request.data['username'], email= request.data['email'])

        if created:
            djangostudent = DjangoStudent(user=user, username=request.data['username'])
            djangostudent.save()

            user.set_password(request.data['password'])
            user.save()
            return JsonResponse({'message': 'User Created Successfully go to Login'})
        else:
            return JsonResponse({'message': 'Error: User with that Email already registered'})


def jwt_response_payload_handler(token, user=None, request=None):
    
        
    return {
        'token': token,
        'name': user.username,
        'id': user.id
    }




