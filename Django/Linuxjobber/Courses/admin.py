from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.http import HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.shortcuts import redirect
from django.contrib import admin, messages
from django.urls import path
from subprocess import PIPE, run
import subprocess
import sys
import configparser
import ast
import os, shutil
from decouple import config, Csv
from email.parser import Parser
from .models import *
from home.mail_service import LinuxjobberMailer, LinuxjobberMassMailer

class CourseTopicAdmin(admin.ModelAdmin):
	search_fields = ('course__course_title','topic',)
	list_display = ('topic','course')

class CoursePermissionAdmin(admin.ModelAdmin):
	search_fields = ('user__username','user__email',)
	list_display = ('user','course','permission','expiry_date')

class LabTaskAdmin(admin.ModelAdmin):
	search_fields = ('lab__topic',)

class NoteAdminForm(forms.ModelForm):
	Detail = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = Note
		fields = ['Topic','Detail'] 

class NoteAdmin(admin.ModelAdmin):
	form = NoteAdminForm

class UserInterestAdmin(admin.ModelAdmin):
	list_display = ('user', 'course')

class UserCourseStatAdmin(admin.ModelAdmin):
	list_display = ('user', 'course', 'visit')

class GradesReportAdmin(admin.ModelAdmin):
	list_display = ('user','course_topic','grade')
	actions = ['send_lab_report']
	change_list_template = 'admin/send_lab_reports.html'

	def get_urls(self):
		urls = super().get_urls()
		# my_urls = [
		# 	path('', self.clean_mail, name= 'clean-mail-log'),
		#]  # type: List[path]
		return   urls

	def send_lab_report(self, request, queryset):
		instructors = ast.literal_eval(config('INSTRUCTORS')) 
		print(instructors)
		sets = []
		sets_value = []
		for obj in queryset:
			if str(obj) not in sets_value:
				sets_value.append(str(obj))
				sets.append(obj)
		# output = run([sys.executable, 'C:\\Users\\USER\Documents\\linuxjobber2\\Django\\Linuxjobber\\Courses\\daily.py',
		#             '1', 'k'], shell=False, stdout=PIPE)
		output = subprocess.check_output('python ./Courses/daily.py 1 k all', shell=True).splitlines()
		# print(output)
		for person in sets:
			if str(person.course_topic.course) == 'Linux Fundamentals':
				user = str(person)
				user = user.split('@')[0]
				message = b''
				for report in output:
					if user.encode('utf-8') in report:

						message += report + b'\n'
				recievers = instructors +  [str(person)]
				
				for receiver in recievers:
					mailer = LinuxjobberMailer(
						        subject=" Current Fundamentals Lab Report for %s"%(user),
								to_address=receiver,
								header_text="Linuxjobber",
								type=None,
								message=message.decode('utf-8')
					)	
					mailer.send_mail()	
				messages.success(request,'Lab reports have been sent successfully')	
			elif str(person.course_topic.course) == 'Linux Proficiency':
				user = str(person)
				user = user.split('@')[0]
				message = b''
				for report in output:
					if user.encode('utf-8') in report:

						message += report + b'\n'
				recievers = instructors +  [str(person)]

				for receiver in recievers:
					mailer = LinuxjobberMailer(
						        subject=" Current Proficiency Lab Report for %s"%(user),
								to_address=receiver,
								header_text="Linuxjobber",
								type=None,
								message=message.decode('utf-8')
					)	
					mailer.send_mail()	
				messages.success(request,'Lab reports have been sent successfully')				
			elif str(person.course_topic.course) == 'Devops':
				user = str(person)
				user = user.split('@')[0]
				message = b''
				for report in output:
					if user.encode('utf-8') in report:

						message += report + b'\n'
				recievers = instructors +  [str(person)]

				for receiver in recievers:
					mailer = LinuxjobberMailer(
						        subject=" Current Devops Lab Report for %s"%(user),
								to_address=receiver,
								header_text="Linuxjobber",
								type=None,
								message=message.decode('utf-8')
					)	
					mailer.send_mail()	
				messages.success(request,'Lab reports have been sent successfully')						
			else:
				messages.success(request,'Lab reports have been sent successfully')
				print('nay')
		
		# return TemplateResponse(request,'admin/send_lab_reports.html')

		
	send_lab_report.short_description = "Send lab reports to students and instructors"

class LabTaskAdmin(admin.ModelAdmin):
	list_display = ('task', 'lab')

class TopicStatAdmin(admin.ModelAdmin):
	list_display = ('user','topic','last_watched')
	search_fields = ('user__email',)

class CourseSectionAdmin(admin.ModelAdmin):
	list_display = ('course', 'name')

class CourseFeedbackAdmin(admin.ModelAdmin):
	list_display = ('course', 'user' , 'rating','comment', 'created_on','updated_on')

admin.site.register(Course)
admin.site.register(CourseTopic, CourseTopicAdmin)
admin.site.register(CourseDescription)
admin.site.register(CoursePermission, CoursePermissionAdmin)
admin.site.register(LabTask, LabTaskAdmin)
admin.site.register(GradesReport, GradesReportAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(NoteComment)
admin.site.register(TopicStat,TopicStatAdmin)
admin.site.register(UserInterest,UserInterestAdmin)
admin.site.register(UserCourseStat,UserCourseStatAdmin)
admin.site.register(CourseSection,CourseSectionAdmin)
admin.site.register(CourseFeedback,CourseFeedbackAdmin)
