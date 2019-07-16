from django.contrib import admin
from django import forms
from . import models
from django.core.mail import send_mail
from django.conf import settings
from .models import FAQ, Job, RHCSAOrder,FreeAccountClick,  Campaign, Message, Unsubscriber, Internship, InternshipDetail, MessageGroup, UserLocation, NewsLetterSubscribers, UserOrder, Document, MainModel, AwsCredential, Jobplacement, Groupclass, BillingHistory, GroupClassRegister, StripePayment, UserPayment, wepeoples, wetask, werole, wework, wetype, PartTimeJob, TryFreeRecord, FullTimePostion, PartTimePostion, Resume
from datetime import timedelta
import datetime
import subprocess, os

class weworkAdmin(admin.ModelAdmin):
	search_fields = ['we_people__user__email']
	raw_id_fields = ['task']
	list_filter = ('status',)
	list_display = ['we_people','weight','task','status','due','task_type']

	def task_type(self, obj):
		return obj.task.types

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if db_field.name == "task":
			kwargs["queryset"] = wetask.objects.filter(is_active=1)
		return super().formfield_for_manytomany(db_field, request, **kwargs)

	def save_model(self, request, obj, form, change):
		#check if start date is added already
		weprof = wepeoples.objects.get(user=obj.we_people.user)
		if not weprof.start_date:
			weprof.start_date = datetime.datetime.now()
			weprof.graduation_date = datetime.datetime.now() + timedelta(days=90)
			weprof.save(update_fields=["start_date","graduation_date"])
		#send task to user
		if obj.send_task == 1:
			task = wetask.objects.get(pk=form.cleaned_data['task'].id)
			send_mail('Linuxjobber WE Task: '+task.task, 'Hello '+obj.we_people.user.first_name+ ', \n\nTask: '+task.task +'\n\n objective: '+task.objective+'\n\n Description: '+task.description+' .\n\n Thanks & Regards \n Linuxjobber', settings.EMAIL_HOST_USER, [obj.we_people.user.email])

		super().save_model(request, obj, form, change)

class campaignAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):

		if obj.send_message == 1:
			outps = None
			outs = None
			print('okay passed')
			if obj.Target == 0:
				Role = "all_role6"
			elif obj.Target == 1:
				Role = "all_role4"
			elif obj.Target == 2:
				Role = "nigerian_internship"
			elif obj.Target == 3:
				Role = "part_time_fresh_grads"
			elif obj.Target == 4:
				Role = "marketing_internship"
			
			outps = subprocess.Popen(["sshpass","-p", 'dead123linux', "ssh", "-o StrictHostKeyChecking=no", "-o LogLevel=ERROR", "-o UserKnownHostsFile=/dev/null", "sysadmin3@52.41.75.77", "python /oldtools/campaigns/composeMail.py", '1', Role, str(obj.message.slug)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
			outs = subprocess.Popen(["sshpass","-p", 'dead123linux', "ssh", "-o StrictHostKeyChecking=no", "-o LogLevel=ERROR", "-o UserKnownHostsFile=/dev/null", "sysadmin3@52.41.75.77", "python /tools/campaigns/composeMail.py", '1', Role, str(obj.message.slug)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
			print(outps)
			print(outs)

		print(obj.message.slug)
		print(obj.send_message)
		print(obj.Target)

		super().save_model(request, obj, form, change)		
	

class wetaskAdmin(admin.ModelAdmin):
	search_fields = ['types__types','task']
	list_display = ['task','weight', 'is_active', 'types','group']
	list_filter = ('types__types','is_active',)

class MessageAdmin(admin.ModelAdmin):
	search_fields = ['group']
	list_display = ['title','slug','group']
	list_filter = ('group',)

admin.site.register(FAQ)
admin.site.register(Job)
admin.site.register(UserOrder)
admin.site.register(Document)
admin.site.register(MainModel)
admin.site.register(AwsCredential)
admin.site.register(Jobplacement)
admin.site.register(Groupclass)
admin.site.register(GroupClassRegister)
admin.site.register(BillingHistory)
admin.site.register(RHCSAOrder)
admin.site.register(Campaign,campaignAdmin)
admin.site.register(NewsLetterSubscribers)
admin.site.register(StripePayment)
admin.site.register(UserLocation)
admin.site.register(Internship)
admin.site.register(InternshipDetail)
admin.site.register(UserPayment)
admin.site.register(Unsubscriber)
admin.site.register(wepeoples)
admin.site.register(Message,MessageAdmin)
admin.site.register(MessageGroup)
admin.site.register(PartTimeJob)
admin.site.register(FullTimePostion)
admin.site.register(PartTimePostion)
admin.site.register(wetask,wetaskAdmin)
admin.site.register(wework,weworkAdmin)
admin.site.register(wetype)
admin.site.register(FreeAccountClick)
admin.site.register(werole)
admin.site.register(Resume)
admin.site.register(TryFreeRecord)
