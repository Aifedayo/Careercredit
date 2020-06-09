import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import CustomUser
from django.core.files.storage import FileSystemStorage
from django.core.validators import MaxValueValidator

from subprocess import PIPE, run
import subprocess
import sys
import configparser
import ast
import os, shutil
from decouple import config, Csv

fs = FileSystemStorage(location='/media/uploads')

LAB_SUBMISSION= (
		(0, 'none'),
		(1, 'submit by uploading document'),
		(2, 'submit by machine ID'),
		(3, 'submit from repo')
	)

class Course(models.Model):
	course_title = models.CharField(max_length = 200)
	lab_submission_type = models.PositiveSmallIntegerField(default=1, choices=LAB_SUBMISSION)
	aws_credential_required = models.IntegerField(default=0 ,choices=((0, 'No'), (1, 'Yes')))
	icon = models.CharField(max_length = 200, null=True)
	has_certification =  models.IntegerField(default=0 ,choices=((0, 'No'), (1, 'Yes')))
	weight = models.IntegerField(unique=True, null=True)

	
	class Meta:
		verbose_name_plural = 'Courses'
		ordering = ('weight',)
	
	def __str__(self):
		return self.course_title

class CoursePermission(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	user = models.ForeignKey(CustomUser,on_delete = models.CASCADE, limit_choices_to={'role': 4})
	permission = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))
	expiry_date = models.DateTimeField(default=timezone.now, null=False)

	def __str__(self):
		return self.user.email


class CourseTopic(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name='topics',related_query_name='topic')
	section = models.ForeignKey("CourseSection", on_delete = models.DO_NOTHING, null= True)
	topic_number = models.PositiveSmallIntegerField(default=0)
	topic =  models.CharField(max_length = 200)
	lab_name = models.CharField(max_length = 50)
	video = models.TextField()
	description = models.TextField(default="nil")
	lab_description = models.TextField(null=True)
	has_notes = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))
	has_labs = models.IntegerField(default=1 ,choices=((0, 'No'), (1, 'Yes')))
	free = models.IntegerField(default=0 ,choices=((0, 'No'), (1, 'Yes')))
	duration =  models.IntegerField(default=55)
	
	class Meta:
		verbose_name_plural = 'Course Topics'
		
	def __str__(self):
		return self.topic

	def get_status(self):
		return self.topicstatus_set.filter()


class TopicStat(models.Model):
	topic = models.ForeignKey(CourseTopic, on_delete = models.CASCADE)
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	video = models.IntegerField(default=0, validators=[MaxValueValidator(25)])
	status = models.CharField(default='start_video',max_length = 200)
	last_watched = models.DateTimeField(default=timezone.now, null=False)

	def __str__(self):
		return self.user.email


	def videos_watched_is_true(self, count:int, user:CustomUser, course:Course) -> bool:
		"""
		Used to validate if X number of videos has been watched
		:param count:
		:param user:
		:param course:
		:return: True|false
		"""
		if count == None:
			count = 4
		if TopicStat.objects.filter(user=user,topic__course= course).count() >= count:
			return True
		return False

class Note(models.Model):
	Topic = models.OneToOneField(CourseTopic, on_delete = models.CASCADE)
	Detail = models.TextField()

	def __str__(self):
		return self.Topic.topic

class NoteComment(models.Model):
	User = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	Note = models.ForeignKey(Note, on_delete = models.CASCADE)
	Comment = models.CharField(max_length = 200)
	date_created = models.DateTimeField(default=timezone.now, null=False)

	def __str__(self):
		return self.Comment


class CourseDescription(models.Model):
	course = models.OneToOneField(Course, on_delete = models.CASCADE)
	course_detail = models.TextField()
	why_course = models.TextField()
	opportunity = models.TextField()
	prerequisite = models.TextField()
	course_duration = models.PositiveSmallIntegerField()
	study_plan = models.TextField()
	salary = models.IntegerField(default=0)
	salary_source = models.CharField(max_length = 200)
	syllabus_content = models.TextField()
	syllabus_topic = models.TextField()
	certificate = models.CharField(max_length = 20)
	
	def __str__(self):
		return self.course.course_title 


class LabTask(models.Model):
	lab = models.ForeignKey(CourseTopic, on_delete = models.CASCADE, related_name='tasks',related_query_name='task')
	task_number = models.PositiveSmallIntegerField()
	comment = models.TextField()
	note = models.TextField(null = True, blank = True)
	task = models.TextField()
	xpected = models.TextField(default="Nil")
	hint = models.TextField(null = True, blank = True)
	instruction = models.TextField()
	
	class Meta:
		verbose_name_plural = 'Lab Tasks'
		ordering = ('lab_id', 'task_number')
		
	def __str__(self):
		return self.task

class UserInterest(models.Model):
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	date_created = models.DateTimeField(default=timezone.now, null=False)

	class Meta:
		ordering = ('user', 'course')

	def __str__(self):
		return self.user.email

class UserCourseStat(models.Model):
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	visit = models.IntegerField()
	date_created = models.DateTimeField(default=timezone.now, null=False)

	class Meta:
		ordering = ('user', 'course')
	
	def __str__(self):
		return self.user.email
	
	
class GradesReport(models.Model):
	date = models.DateTimeField(default=timezone.now, null=False)
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	course_topic = models.ForeignKey(CourseTopic, on_delete = models.CASCADE, related_name='grades',related_query_name='grade')
	score = models.PositiveSmallIntegerField(default=0)
	grade = models.CharField(default='not graded', max_length=20)
	lab = models.ForeignKey(LabTask, on_delete = models.CASCADE)
	
	class Meta:
		verbose_name_plural = 'Grades Reports'
	
	def __str__(self):
		return self.user.email

	@staticmethod
	def send_lab_report():
		from .utilities import get_query
		instructors = ast.literal_eval(config('INSTRUCTORS')) 
		# print(instructors)
		fundamentalsStudents = GradesReportsReceiver.objects.get(name='Linux Fundamentals').receivers.all()
		proficiencyStudents = GradesReportsReceiver.objects.get(name='Linux Proficiency').receivers.all()
		onPremStudents=GradesReportsReceiver.objects.get(name='Devops').receivers.all()
		# sets = []
		# sets_value = []
		# reports_receivers = GradesReportsReceiver.objects.all()[0]
		# queryset = reports_receivers.receivers.all()
		# print(queryset)
		# for obj in queryset:
			# person = GradesReport.objects.filter(user=obj)
		# output = run([sys.executable, 'C:\\Users\\USER\Documents\\linuxjobber2\\Django\\Linuxjobber\\Courses\\daily.py',
		#             '1', 'k'], shell=False, stdout=PIPE)
		try:
			output = subprocess.check_output('python ./Courses/daily.py 1 k all', shell=True).splitlines()
		except:
			output = subprocess.check_output('python3.6 ./Courses/daily.py 1 k all', shell=True).splitlines()

		fundamentalsReports =''
		proficiencyReports =''
		onPremReports= ''
		for student in fundamentalsStudents:
			# print(output)
			user = str(student)
			user = user.split('@')[0]
			message = b''
			for report in output:
					if user.encode('utf-8') in report and 'LinuxFundamentalsLab_'.encode('utf-8') in report :
						message += report + b'\n'
			recievers =instructors + [str(student)]  
			print(recievers)
			if message:
				from home.mail_service import LinuxjobberMailer
				for receiver in recievers:
					mailer = LinuxjobberMailer(
								subject=" Current Fundamentals Lab Report for %s"%(user),
								to_address=receiver,
								header_text="Linuxjobber",
								type=None,
								message=message.decode('utf-8')
					)	
					mailer.send_mail()
				print('sent')
		for student in proficiencyStudents:
			print(student)
			user = str(student)
			user = user.split('@')[0]
			message = b''
			for report in output:
					if user.encode('utf-8') in report and 'LinuxProficiencyLab_'.encode('utf-8') in report:
						message += report + b'\n'
			recievers = instructors + [str(student)] 
			if message: 
				from home.mail_service import LinuxjobberMailer
				for receiver in recievers:
					mailer = LinuxjobberMailer(
								subject=" Current Proficiency Lab Report for %s"%(user),
								to_address=receiver,
								header_text="Linuxjobber",
								type=None,
								message=message.decode('utf-8')
					)	
					mailer.send_mail()

		for student in onPremStudents:
			print(student)
			user = str(student)
			user = user.split('@')[0]
			message = b''
			for report in output:
					if user.encode('utf-8') in report and 'OnPremDeployment_'.encode('utf-8') in report:
						message += report + b'\n'
			recievers = instructors + [str(student)]  
			if message:
				from home.mail_service import LinuxjobberMailer
				for receiver in recievers:
					mailer = LinuxjobberMailer(
								subject=" Current Devops Lab Report for %s"%(user),
								to_address=receiver,
								header_text="Linuxjobber",
								type=None,
								message=message.decode('utf-8')
					)	
					mailer.send_mail()

		# for per in sets:
		# 	print(person)
		# 	if str(person.course_topic.course) == 'Linux Fundamentals':
		# 		print('sets')
		# 		user = str(person)
		# 		user = user.split('@')[0]
		# 		message = b''
		# 		for report in output:
		# 			if user.encode('utf-8') in report:

		# 				message += report + b'\n'
		# 		recievers =[str(person)] + instructors 
		# 		from home.mail_service import LinuxjobberMailer
		# 		for receiver in recievers:
		# 			mailer = LinuxjobberMailer(
		# 						subject=" Current Fundamentals Lab Report for %s"%(user),
		# 						to_address=receiver,
		# 						header_text="Linuxjobber",
		# 						type=None,
		# 						message=message.decode('utf-8')
		# 			)	
		# 			mailer.send_mail()
				
		# 		# messages.success(request,'Lab reports have been sent successfully')	
		# 	elif str(person.course_topic.course) == 'Linux Proficiency':
		# 		print('hi')
		# 		user = str(person)
		# 		user = user.split('@')[0]
		# 		message = b''
		# 		for report in output:
		# 			if user.encode('utf-8') in report:

		# 				message += report + b'\n'
		# 		recievers = instructors +  [str(person)]

		# 		for receiver in recievers:
		# 			mailer = LinuxjobberMailer(
		# 						subject=" Current Proficiency Lab Report for %s"%(user),
		# 						to_address=receiver,
		# 						header_text="Linuxjobber",
		# 						type=None,
		# 						message=message.decode('utf-8')
		# 			)	
		# 			mailer.send_mail()	
		# 		# messages.success(request,'Lab reports have been sent successfully')				
		# 	elif str(person.course_topic.course) == 'Devops':
		# 		print('hey')
		# 		user = str(person)
		# 		user = user.split('@')[0]
		# 		message = b''
		# 		for report in output:
		# 			if user.encode('utf-8') in report:

		# 				message += report + b'\n'
		# 		recievers = instructors +  [str(person)]

		# 		for receiver in recievers:
		# 			mailer = LinuxjobberMailer(
		# 						subject=" Current Devops Lab Report for %s"%(user),
		# 						to_address=receiver,
		# 						header_text="Linuxjobber",
		# 						type=None,
		# 						message=message.decode('utf-8')
		# 			)	
		# 			mailer.send_mail()	
		# 		# messages.success(request,'Lab reports have been sent successfully')						
		# 	else:
		# 		# messages.success(request,'Lab reports have been sent successfully')
		# 		print('nay')

def content_file_name(instance, filename):
	ext = ''
	if instance.course_topic.topic_number == 4:
		ext = 'py'
	elif instance.course_topic.topic_number > 4 and instance.course_topic.topic_number < 7 :
		ext = 'sql'
	else:
		if filename.endswith('.zip'):
			ext = 'zip'
		elif filename.endswith('tar'):
			ext = 'tar'
		else:
			ext = 'gz'
	filename = "%s_%s.%s" % (instance.user.username, instance.course_topic.topic_number, ext)
	return os.path.join('uploads', filename)


class Document(models.Model):
	course_topic = models.ForeignKey(CourseTopic, on_delete = models.CASCADE)
	user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
	document = models.FileField(upload_to = content_file_name )
	uploaded_at = models.DateTimeField(auto_now_add = True)


class MainModel(models.Model):
	title = models.CharField(max_length = 42)
	document = models.ForeignKey(Document, on_delete = models.CASCADE)


class CourseSection(models.Model):
	"""
		Course Section
		A course can be split into sections.
		E.g Linux Proficiency can have File Management Section, Monitoring Services Section, etc.

	"""
	course = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
	name = models.CharField(max_length=500)

	def __str__(self):
		return self.name

class CourseFeedback(models.Model):
	"""
		Linuxjobber feedback model.
		User feedback on courses go here

	"""
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
	rating = models.IntegerField(default=0)
	comment =  models.TextField()
	created_on = models.DateTimeField(null=True,auto_now_add=True)
	updated_on = models.DateTimeField(null=True,auto_now=True)

	def __str__(self):
		return " {course}: {rating} stars  ".format(
			course = self.course.course_title,
			rating = self.rating
		)

class GradesReportsReceiver(models.Model):
	name = models.CharField(('name'), max_length=80, unique=True)
	receivers = models.ManyToManyField(
        CustomUser,
        verbose_name=('receivers'),
        blank=True,
    )
	def __str__(self):
		return self.name
		