from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Role(models.Model):
    role = models.IntegerField()
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{role} ({description})".format(role=self.role, description = self.description)


class CustomUser(AbstractUser):
    # is_subscribed  = models.IntegerField(default=1,choices=((0, 'No'), (1, 'Yes')))
    role = models.IntegerField(default=6)
    profile_img = models.TextField(
        default='https://res.cloudinary.com/louiseyoma/image/upload/v1546701687/profile_pic.png')
    pwd_reset_token = models.CharField(max_length=100, default='000011112222')
    # user_role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True)
    available_roles = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.email

    def update_role(self):
        if self.role:
            role,created = Role.objects.get_or_create(role=self.role)
            self.available_roles = role
        else:
            role, created = Role.objects.get_or_create(role=6)
            self.role = role.role
            self.available_roles = role

    def save(self,*args,**kwargs):
        """
        Sets user role from the role field
        :param args:
        :param kwargs:
        :return:
        """
        self.update_role()
        super(type(self),self).save(*args, **kwargs)
