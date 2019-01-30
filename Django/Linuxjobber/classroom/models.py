from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User
from users.models import CustomUser

# Create your models here.

class DjangoStudent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']


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


class ChatUpload(models.Model):
  upload = models.FileField(upload_to='chat_uploads')

