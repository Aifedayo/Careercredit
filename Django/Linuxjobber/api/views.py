from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view

from Courses import models
from . import serializers
# Create your views here.

class ListCourses(generics.ListCreateAPIView):
	queryset = models.Course.objects.all()
	serializer_class = serializers.CourseSerializer


class DetailCourse(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Course.objects.all()
	serializer_class = serializers.CourseSerializer


class ListUser(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = serializers.UserSerializer


class DetailUser(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = serializers.UserSerializer

@api_view()
def token_owner(request, tkn):
	owner_inst = Token.objects.get(key=tkn)
	owner = User.objects.get(pk=owner_inst.user_id)
	return Response({"user":owner.username})


'''class CustomAuthToken(ObtainAuthToken):

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception = True)
		user = serializer.validate_data['user']
		token = Token.objects.get(user=user)
		return Response({'token': token.key, 'username': username})'''