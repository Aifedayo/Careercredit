from django.db import models
from classroom.models import ChatRoom

class User(models.Model):
    username = models.CharField(max_length=100,unique=True)
    profile_img = models.TextField(
        default='https://res.cloudinary.com/louiseyoma/\
        image/upload/v1546701687/profile_pic.png'
    )    

    class Meta:
        db_table = "users_customuser"
        managed = False

class ChatMessageWithProfile(models.Model):
    user = models.ForeignKey(
        User,  db_column='user',
        to_field='username', on_delete=models.CASCADE
    )

    message = models.CharField(max_length=400)
    the_type=models.CharField(max_length=10,default='plain')
    timestamp=models.CharField(max_length=100,null=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null = True)

    class Meta:
        db_table = "classroom_chatmessage"
        managed = False