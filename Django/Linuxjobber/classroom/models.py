from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from users.models import CustomUser

# Create your models here.
from home.models import Groupclass


class DjangoStudent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']


class Course(models.Model):
    course_id = models.IntegerField(unique=True)
    course_title = models.CharField(max_length=100)
    course_description = models.CharField(max_length=300)
    course_video = models.IntegerField()
    registered_students = models.IntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    course_image = models.ImageField(upload_to='classroom', null=True)

    def __str__(self):
        return self.course_title

class CourseTopic(models.Model):
    topic_id = models.IntegerField()
    topic_title = models.CharField(max_length=200)
    topic_video = models.CharField(max_length=100)
    topic_course = models.ForeignKey(Course,on_delete=models.CASCADE)
    has_notes = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))
    has_labs = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))

    def __str__(self):
        return self.topic_title

class ChatRoom(models.Model):
    name = models.CharField(max_length=60)
    hash = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    user = models.CharField(max_length=50)
    message = models.CharField(max_length=400)
    the_type=models.CharField(max_length=10,default='plain')
    timestamp=models.CharField(max_length=100,null=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null = True)

    def save(self, *args, **kwargs):
        super(ChatMessage, self).save(*args, **kwargs)
        return self

class ChatUpload(models.Model):
  upload = models.FileField(upload_to='chat_uploads')


class AttendanceLog(models.Model):
    group=models.ForeignKey(Groupclass,on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_query_name='group_attendance')
    timestamp=models.CharField(max_length=100)
    video_url=models.URLField(null=True,blank=True)

class Connection(models.Model):
    connection_id = models.CharField(max_length=255)

