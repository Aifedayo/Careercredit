from rest_framework import serializers
from home.models import Groupclass
from users.models import CustomUser

from Courses.models import Course

from Courses.models import CourseTopic

from Courses.models import LabTask

from Courses.models import Note

from classroom.models import AttendanceLog




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','email','first_name','last_name','profile_img','role']

class GroupUserSerializer(serializers.ModelSerializer):
    user=UserSerializer(many=True)
    class Meta:
        fields= ['last_login','user']

        # fields = ['id','username','email','first_name','last_name']
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
    class Meta:
        model = LabTask
        fields = "__all__"

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=AttendanceLog
        fields=['timestamp','video_url']

class UserAttendaceSerializer(serializers.ModelSerializer):

    group_attendance = AttendanceSerializer(many=True)
    class Meta:
        model = CustomUser
        fields=['group_attendance','user']

class CourseSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["topics"]
class GroupClassSerializer(serializers.ModelSerializer):
    course=CourseSerializer2()
    class Meta:
        model = Groupclass
        fields = "__all__"

class NoteSerializer(serializers.ModelSerializer):
    Topic=serializers.StringRelatedField()
    class Meta:
        model = Note
        fields = ['Detail','Topic']
