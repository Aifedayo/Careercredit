from rest_framework import serializers
from home.models import Groupclass
from users.models import CustomUser

from Courses.models import Course

from Courses.models import CourseTopic

from Courses.models import LabTask

from Courses.models import Note


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

class LabTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTask
        fields = ['id','comment','note','task','hint','instruction']

class CourseNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id','note']

class CourseTopicSerializer(serializers.ModelSerializer):
    tasks=LabTaskSerializer(many=True)
    # tasks=serializers.SerializerMethodField()
    note= serializers.StringRelatedField()
    class Meta:
        model = CourseTopic
        fields = ['id','topic','video','tasks','note']
        ordering="id"

class CourseSerializer(serializers.ModelSerializer):
    topics=CourseTopicSerializer(many=True)
    class Meta:
        model = Course
        fields = "__all__"

class TopicLabSerializer(serializers.ModelSerializer):
    course=CourseSerializer()
    class Meta:
        model = CourseTopic
        fields = "__all__"
        ord


