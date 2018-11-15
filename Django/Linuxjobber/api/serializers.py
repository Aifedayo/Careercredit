from rest_framework import serializers
from Courses import models
from django.contrib.auth.models import User

class CourseSerializer(serializers.ModelSerializer):

	class Meta:
		fields = (
			'id',
			'course_title',
			)
		model = models.Course


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		fields = (
			'id',
			'username',
			'email',
			)
		model = User

	