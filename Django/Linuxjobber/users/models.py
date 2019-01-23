from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
	role = models.IntegerField(default=6)
	profile_img = models.TextField(default='https://res.cloudinary.com/louiseyoma/image/upload/v1546701687/profile_pic.png')
	pwd_reset_token = models.CharField(max_length=100,default='000011112222')
	allowed_project = models.IntegerField(default=1)

	def __str__(self):
		return self.email

