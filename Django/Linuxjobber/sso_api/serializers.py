from rest_framework import serializers
from home.models import Groupclass
from users.models import CustomUser

from Courses.models import Course

from Courses.models import CourseTopic


class GroupClassSerializer(serializers.ModelSerializer):
    course=serializers.StringRelatedField()
    users=serializers.StringRelatedField(many=True)
    class Meta:
        model = Groupclass
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class CourseTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseTopic
        fields = "__all__"
        depth=1