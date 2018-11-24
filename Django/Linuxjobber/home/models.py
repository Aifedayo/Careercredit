import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from users.models import CustomUser


class FAQ(models.Model):
    question = models.CharField(max_length = 200)
    response = models.CharField(max_length = 1000)
    
    class Meta:
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return self.question


class Job(models.Model):

    POSITION = (
        (1, 'Part-time Frontend Developer'),
        (2, 'Web Frontend Developer'),
        (3, 'AWS Cloud Architecture'),
        (4, 'Linux Administrator'),
        (5, 'Part-time Java Developer'),
    )

    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    position = models.IntegerField(default=1, choices=POSITION) 
    resume = models.FileField(upload_to = 'resume')

    def __str__(self):
        return self.firstname +' ' +self.lastname


def content_file_name(instance, filename):
    return os.path.join('uploads', 'resumes', instance.user.username+'_'+filename)


class Jobplacement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1) 
    education = models.CharField(max_length = 70)
    career =  models.CharField(max_length = 100)
    resume = models.FileField(upload_to = content_file_name )
    placement_grade = models.PositiveSmallIntegerField(default=0)
    experience = models.IntegerField(default=0)
    is_certified = models.CharField(max_length = 50)
    training = models.CharField(max_length = 50)
    can_relocate = models.CharField(max_length = 50)
    awareness = models.CharField(max_length= 200)
    date = models.DateTimeField(default=timezone.now, null=False)
    
    class Meta:
        verbose_name_plural = 'Jobplacement Applications'
    
    def __str__(self):
        return self.user.email


class UserPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, related_name='payments',related_query_name='payment')
    amount = models.IntegerField(default=0)
    trans_id = models.CharField(max_length = 100)
    pay_for = models.CharField(max_length = 100)
    paid_at = models.DateTimeField(default=timezone.now, null=False)
    
    class Meta:
        verbose_name_plural = 'User Payments'
        
    def __str__(self):
        return self.user.username + ' ' + self.pay_for + '_' +self.trans_id

class Groupclass(models.Model):
    name = models.CharField(max_length = 200)
    start_date = models.CharField(max_length = 100)
    end_date = models.CharField(max_length= 100)
    duration = models.CharField(max_length= 10)
    price = models.IntegerField(default=0)
    class_meet = models.CharField(max_length= 50)
    type_of_class = models.CharField(max_length= 100)
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.name

class GroupClassRegister(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_paid = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    type_of_class = models.CharField(max_length= 100)
    date = models.DateTimeField(default=timezone.now, null=False)


    def __str__(self):
        return self.user.email

class StripePayment(models.Model):
    secretkey = models.TextField()
    publickey = models.TextField()
    planid = models.TextField()

    def __str__(self):
        return self.secretkey


class BillingHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    subscription_id = models.CharField(max_length= 100)
    status = models.CharField(max_length= 100)
    date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return self.user.email    

class ContactMessages(models.Model):
    full_name = models.CharField(max_length = 200)
    email = models.EmailField(max_length = 200)
    phone_no = models.CharField(max_length = 20)
    message_subject = models.CharField(max_length = 200)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'ContactMessages'

    def __str__(self):
        return self.subject




class Document(models.Model):
	document = models.FileField(upload_to = 'uploads/' )
	uploaded_at = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.id

class MainModel(models.Model):
    title = models.CharField(max_length = 42)
    document = models.ForeignKey(Document, on_delete = models.CASCADE)

class AwsCredential(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	username = models.CharField(max_length=200)
	accesskey = models.CharField(max_length=200)
	secretkey = models.CharField(max_length=200)
	date = models.DateTimeField(default=timezone.now, null=False)
	
	def __str__(self):
		return self.user.username

class Internship(models.Model):
	firstname = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	phone = models.CharField(max_length=50)
	Address = models.CharField(max_length=200)
	college = models.CharField(max_length=200)
	country = models.CharField(max_length=200)
	experience = models.CharField(max_length=50)
	course = models.CharField(max_length=200)
	resume = models.FileField(upload_to = 'resume')

	def __str__(self):
		return self.firstname +' ' +self.lastname


class Resume(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	resume = models.FileField(upload_to = 'resume')

	def __str__(self):
		return self.user.username


class UserOrder(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    order_id = models.CharField(max_length = 20)
    order_amount = models.IntegerField(default=0)
    subscription = models.CharField(max_length = 100)
    status = models.CharField(max_length = 20)
    paid_date = models.DateTimeField(default=timezone.now, null=False)

    class Meta:
        verbose_name_plural = "User Orders"

    def __str__(self):
        return self.user.email


class NewsLetterSubscribers(models.Model):
    email = models.EmailField(max_length = 200)